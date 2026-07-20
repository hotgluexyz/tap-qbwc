"""QBWC base stream with dynamic schema from QBD XSD."""

from __future__ import annotations

from functools import cached_property
from typing import Any, Dict, Set, Iterable, Optional

from hotglue_singer_sdk import Stream, typing as th
from hotglue_singer_sdk.helpers.jsonpath import extract_jsonpath
from xmlschema.validators import XsdElement, XsdType


# QBD named simple types → Singer JSON Schema types
_NAMED_TYPE_MAP: dict[str, type] = {
    "BOOLTYPE": th.BooleanType,
    "DATETIMETYPE": th.DateTimeType,
    "DATETYPE": th.DateType,
    "INTTYPE": th.IntegerType,
    "FLOATTYPE": th.NumberType,
}

_XS_BOOLEAN = "{http://www.w3.org/2001/XMLSchema}boolean"
_XS_INTEGER = "{http://www.w3.org/2001/XMLSchema}integer"
_XS_DECIMAL = "{http://www.w3.org/2001/XMLSchema}decimal"
_XS_DATE = "{http://www.w3.org/2001/XMLSchema}date"


def _local_name(name: str | None) -> str | None:
    if name is None:
        return None
    if "}" in name:
        return name.rsplit("}", 1)[-1]
    return name


def _xsd_simple_to_singer(xsd_type: XsdType) -> Any:
    """Map an XSD simple type to a Singer SDK type class instance."""
    type_name = _local_name(getattr(xsd_type, "name", None))
    if type_name and type_name in _NAMED_TYPE_MAP:
        return _NAMED_TYPE_MAP[type_name]()

    # Walk base/member types for named QBD types and xs builtins
    candidates: list[XsdType] = [xsd_type]
    if getattr(xsd_type, "member_types", None):
        candidates.extend(xsd_type.member_types)

    base = getattr(xsd_type, "base_type", None)
    while base is not None:
        candidates.append(base)
        base_name = _local_name(getattr(base, "name", None))
        if base_name and base_name in _NAMED_TYPE_MAP:
            return _NAMED_TYPE_MAP[base_name]()
        base = getattr(base, "base_type", None)

    for candidate in candidates:
        try:
            primitive = candidate.primitive_type
        except Exception:
            primitive = None
        if primitive is None:
            continue
        prim_name = getattr(primitive, "name", None)
        if prim_name == _XS_BOOLEAN:
            return th.BooleanType()
        if prim_name in (_XS_INTEGER,):
            return th.IntegerType()
        if prim_name == _XS_DECIMAL:
            # INTTYPE restricts xs:integer but reports decimal in some chains;
            # prefer integer only when the named type is INTTYPE (handled above).
            return th.NumberType()
        if prim_name == _XS_DATE:
            return th.DateType()

    return th.StringType()


def _iter_child_elements(xsd_type: XsdType) -> list[XsdElement]:
    content = getattr(xsd_type, "content", None)
    if content is None or not hasattr(content, "iter_elements"):
        return []
    return list(content.iter_elements())


def _complex_to_object(xsd_type: XsdType, seen: Set[int]) -> th.ObjectType:
    """Convert an XSD complex type to a Singer ObjectType."""
    type_id = id(xsd_type)
    if type_id in seen:
        return th.ObjectType()
    seen = seen | {type_id}

    properties: list[th.Property] = []
    for element in _iter_child_elements(xsd_type):
        singer_type = _xsd_element_to_singer(element, seen)
        properties.append(th.Property(element.local_name, singer_type))
    return th.ObjectType(*properties)


def _xsd_element_to_singer(element: XsdElement, seen: Set[int]) -> Any:
    """Convert an XSD element to a Singer type, wrapping arrays when needed."""
    xsd_type = element.type
    if xsd_type.is_complex():
        singer_type: Any = _complex_to_object(xsd_type, seen)
    else:
        singer_type = _xsd_simple_to_singer(xsd_type)

    max_occurs = element.max_occurs
    if max_occurs is None or max_occurs > 1:
        return th.ArrayType(singer_type)
    return singer_type


def _resolve_ret_element(xsd_schema: Any, response_element: str) -> XsdElement:
    """Look up the *Ret child element for a QBXML *Rs response type."""
    type_name = f"{response_element}Type"
    try:
        rs_type = xsd_schema.types[type_name]
    except KeyError as exc:
        raise ValueError(
            f"QBD XML schema has no type named {type_name!r} "
            f"for response_element={response_element!r}"
        ) from exc

    ret_elements = [
        el
        for el in _iter_child_elements(rs_type)
        if el.local_name and el.local_name.endswith("Ret")
    ]
    if not ret_elements:
        raise ValueError(f"No *Ret child element found under XSD type {type_name!r}")
    if len(ret_elements) > 1:
        names = [el.local_name for el in ret_elements]
        raise ValueError(f"Ambiguous *Ret children under XSD type {type_name!r}: {names}")
    return ret_elements[0]


class QWBCBaseStream(Stream):
    """QBWC base stream class."""

    response_element: str
    replication_key_filter_field: str
    page_size: int = 200
    should_paginate: bool = True
    include_line_items = False
    records_jsonpath: str = "$[*]"

    @cached_property
    def selected_properties(self):
        selected_properties = []
        for key, value in self.metadata.items():
            if isinstance(key, tuple) and len(key) == 2 and value.selected:
                field_name = key[-1]
                selected_properties.append(field_name)
        return selected_properties

    def get_replication_key_filter_value(self, context: dict | None) -> str | dict | None:
        if self.replication_key and self.replication_key_filter_field:
            start_date = self.get_starting_time(context)
            start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")

            if self.replication_key_filter_field == "ModifiedDateRangeFilter":
                return {
                    "FromModifiedDate": start_date_str,
                }
            else:
                return start_date_str
        return None

    def prepare_request_payload(
        self, context: dict | None, iterator_id: str | None, is_count_request: bool = False
    ) -> dict | None:
        """
        Prepare the request payload for the QBWC API.

        :param context: The context object.
        :param iterator_id: The iterator ID.
        :param is_count_request: Whether to request the total count of records.
        :return: The request payload.
        """
        request_data = {}
        replication_key_filter_value = self.get_replication_key_filter_value(context)

        if is_count_request:
            request_data["@metaData"] = "MetaDataOnly"
            if replication_key_filter_value:
                request_data[self.replication_key_filter_field] = replication_key_filter_value
        else:
            if self.should_paginate:
                request_data["@iterator"] = "Continue" if iterator_id else "Start"
                if iterator_id:
                    request_data["@iteratorID"] = iterator_id

            request_data["MaxReturned"] = self.page_size

            if self.include_line_items:
                request_data["IncludeLineItems"] = True

            if self.selected_properties:
                request_data["IncludeRetElement"] = self.selected_properties

            if replication_key_filter_value:
                request_data[self.replication_key_filter_field] = replication_key_filter_value

        return {self.request_element: request_data}

    def parse_response(self, response: dict) -> Iterable[dict]:
        yield from extract_jsonpath(self.records_jsonpath, input=response)

    def extract_iterator_id(self, response: dict) -> str | None:
        iterator_id = extract_jsonpath(f"$.{self.response_element}.[0].@iteratorID", input=response)
        return next(iterator_id, None)

    def extract_remaining_records(self, response: dict) -> int:
        remaining_records = extract_jsonpath(
            f"$.{self.response_element}.[0].@iteratorRemainingCount", input=response
        )
        return next(remaining_records, 0)

    def request_records(self, context: dict | None) -> Iterable[dict]:
        iterator_id = None

        while True:
            request_payload = self.prepare_request_payload(context, iterator_id=iterator_id)
            response = self._tap.client.make_request(request_payload)
            yield from self.parse_response(response)

            if not self.should_paginate:
                break

            iterator_id = self.extract_iterator_id(response)
            remaining_records = self.extract_remaining_records(response)
            if not iterator_id or (remaining_records == 0):
                break

            self.logger.info(f"Remaining records: {remaining_records}")

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        for record in self.request_records(context):
            self._tap.client.total_processed_records_count += 1
            transformed = self.post_process(record, context)
            if transformed is not None:
                yield transformed

    def extract_total_count(self, response: dict) -> int:
        total_count = extract_jsonpath(f"$.{self.response_element}.[0].@retCount", input=response)
        return next(total_count, None)

    def get_estimated_record_count(self) -> Optional[int]:
        """Return total_count without mutating sync state."""
        try:
            self._write_starting_replication_value(None)
            request_payload = self.prepare_request_payload(
                context=None, iterator_id=None, is_count_request=True
            )
            response = self._tap.client.make_request(request_payload)
            total_count = self.extract_total_count(response)
            if total_count is not None:
                self._tap.client.total_estimated_records_count += total_count
            self.logger.info(f"Total count: {total_count}")
            return total_count
        except Exception:
            self.logger.info(
                "Skipping estimated record count for stream='%s'",
                self.name,
            )
        return None


class QBWCDynamicSchemaStream(QWBCBaseStream):
    """QBWC dynamic schema stream class."""

    @property
    def schema(self) -> Dict[str, Any]:
        """Build Singer schema from the QBD XSD for ``response_element``."""
        cached = getattr(self, "_schema", None)
        if cached is not None:
            return cached

        if not getattr(self, "response_element", None):
            raise ValueError(f"{type(self).__name__} must define response_element")

        ret_element = _resolve_ret_element(
            self._tap.qbd_xml_schemas,
            self.response_element,
        )
        self.records_jsonpath = f"$.{self.response_element}.[0].{ret_element.local_name}[*]"
        properties = [
            th.Property(
                el.local_name,
                _xsd_element_to_singer(el, set()),
            )
            for el in _iter_child_elements(ret_element.type)
        ]
        self._schema = th.PropertiesList(*properties).to_dict()
        return self._schema
