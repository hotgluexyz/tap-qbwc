import hashlib
import json
import re
import uuid
from functools import lru_cache
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from xml.etree import ElementTree

from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class QBWCTestRunner(VCRTapTestRunner):
    FILTER_HEADERS = [
        *VCRTapTestRunner.FILTER_HEADERS,
        "x-amz-cf-id",
        "x-amzn-trace-id",
        "x-amz-apigw-id",
        "x-amzn-requestid",
        "via",
        "report-to",
        "nel",
    ]
    # Poll status controls completion. XML attributes control errors, counts and pagination;
    # TimeModified is the replication key; transaction queries filter by TxnDate.
    PRESERVE_KEYS = {
        "status",
        "statusCode",
        "statusSeverity",
        "iteratorRemainingCount",
        "retCount",
        "TimeModified",
        "TxnDate",
    }

    @staticmethod
    def fake_id(value):
        # The same session/request/iterator id appears in JSON, URLs and nested XML.
        return str(uuid.uuid5(uuid.NAMESPACE_URL, value))

    def scrub_uri(self, uri):
        parts = urlsplit(uri)
        query = [
            (key, self.fake_id(value) if key in {"session_id", "request_id"} else value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
        ]
        return urlunsplit(parts._replace(query=urlencode(query)))

    @staticmethod
    @lru_cache(maxsize=None)
    def xml_field(path):
        from qbwc_common import load_qbd_xml_schemas

        return load_qbd_xml_schemas().find(path)

    def scrub_response_body(self, body, faker, cache):
        payload = json.loads(body)
        xml = payload.pop("response_payload", None)
        ids = {key: payload.pop(key) for key in ("session_id", "request_id") if key in payload}
        scrubbed = json.loads(super().scrub_response_body(json.dumps(payload), faker, cache))
        scrubbed.update({key: self.fake_id(value) for key, value in ids.items()})
        if xml is not None:
            root = ElementTree.fromstring(xml)
            # Apply the shared XML scrubber, then restore only schema/control values.
            clean = ElementTree.fromstring(super().scrub_response_body(xml, faker, cache))

            def constrain(original, result, path):
                field = self.xml_field(path)
                if original.text and original.text.strip() and not len(original):
                    facets = field.type.facets
                    if "{http://www.w3.org/2001/XMLSchema}enumeration" in facets:
                        # QBXML's strict decoder requires the XSD's public enum literals.
                        result.text = original.text
                    elif re.fullmatch(r"[+-]?\d+(\.\d+)?", original.text):
                        # Monetary/quantity XSD patterns constrain decimal precision.
                        # Fake digits without changing the sign or decimal places.
                        digest = iter(hashlib.sha256(original.text.encode()).digest())
                        result.text = re.sub(r"\d", lambda _: str(next(digest) % 10), original.text)
                    limit = facets.get("{http://www.w3.org/2001/XMLSchema}maxLength")
                    if limit and len(result.text) > limit.value:
                        digest = hashlib.sha256(original.text.encode()).hexdigest()
                        result.text = ("Fake-" + digest)[: limit.value]
                if "iteratorID" in original.attrib:
                    result.set("iteratorID", self.fake_id(original.attrib["iteratorID"]))
                for child, clean_child in zip(original, result):
                    constrain(child, clean_child, f"{path}/{child.tag}")

            constrain(root, clean, root.tag)
            scrubbed["response_payload"] = ElementTree.tostring(clean, encoding="unicode")
        return json.dumps(scrubbed)

    def module(self):
        return "tap_qbwc"

    def launch(self):
        from tap_qbwc.tap import TapQBWC

        TapQBWC.cli()


if __name__ == "__main__":
    QBWCTestRunner.main()
