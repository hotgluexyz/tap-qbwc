"""QBWC tap class."""

from __future__ import annotations
from typing import List, Optional, Union, Any
from pathlib import PurePath, Path

import xmlschema
from hotglue_singer_sdk import Stream, Tap
from hotglue_singer_sdk import typing as th  # JSON schema typing helpers
from typing_extensions import override

from tap_qbwc.client import QBWCClient
from tap_qbwc.streams import (
    AccountsStream,
    ClassesStream,
    CustomersStream,
    VendorsStream,
    ItemsStream,
    InventoryItemsStream,
    ItemSitesStream,
    PriceLevelsStream,
    UnitOfMeasureSetsStream,
    SalesTaxCodesStream,
    ItemSalesTaxesStream,
    BillsStream,
    BillPaymentsCheckStream,
    BillPaymentsCreditCardStream,
    InvoicesStream,
    PurchaseOrdersStream,
    CreditMemosStream,
    SalesOrdersStream,
    SalesReceiptsStream,
    VendorCreditsStream,
    EstimatesStream,
    JournalEntriesStream,
    ChecksStream,
    TransactionsStream,
)


QBD_XML_SCHEMAS_FILE = Path(__file__).parent / "qbd_xml_schemas" / "qbxmlops130.xsd"
STREAM_TYPES = [
    AccountsStream,
    ClassesStream,
    CustomersStream,
    VendorsStream,
    ItemsStream,
    InventoryItemsStream,
    ItemSitesStream,
    PriceLevelsStream,
    UnitOfMeasureSetsStream,
    SalesTaxCodesStream,
    ItemSalesTaxesStream,
    BillsStream,
    BillPaymentsCheckStream,
    BillPaymentsCreditCardStream,
    InvoicesStream,
    PurchaseOrdersStream,
    CreditMemosStream,
    SalesOrdersStream,
    SalesReceiptsStream,
    VendorCreditsStream,
    EstimatesStream,
    JournalEntriesStream,
    ChecksStream,
    TransactionsStream,
]


class TapQBWC(Tap):
    """Singer tap for QBWC."""

    name = "tap-qbwc"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
            default="2000-01-01T00:00:00Z",
        ),
        th.Property(
            "token", th.StringType, required=True, description="The token to access the QBWC API"
        ),
        th.Property(
            "request_timeout",
            th.IntegerType,
            default=1200,
            description="How long to wait for a QBWC request to complete in seconds",
        ),
        th.Property(
            "qbwc_is_alive_timeout",
            th.IntegerType,
            default=3600,
            description="How long to wait for a QBWC is alive request to complete in seconds",
        ),
        th.Property(
            "is_sandbox",
            th.BooleanType,
            default=False,
            description="Whether to use the sandbox environment",
        ),
    ).to_dict()

    def __init__(
        self,
        config: Optional[Union[dict, PurePath, str, List[Union[PurePath, str]]]] = None,
        catalog: Union[PurePath, str, dict, None] = None,
        state: Union[PurePath, str, dict, None] = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        super().__init__(config, catalog, state, parse_env_config, validate_config)

        self.qbd_xml_schemas = self.load_qbd_xml_schemas()
        self.client: QBWCClient = QBWCClient(self.config, self.qbd_xml_schemas, self.logger)

    def run_sync(self, catalog: Any = None, state: Any = None) -> None:
        self.client.create_session()
        self.client.check_qbwc_is_alive()
        super().run_sync(catalog, state)

    def load_qbd_xml_schemas(self) -> xmlschema.XMLSchema:
        """Load the QBD XML schemas."""
        self.logger.info(f"Loading QBD XML schemas from {QBD_XML_SCHEMAS_FILE}")
        self.qbd_xml_schemas = xmlschema.XMLSchema(QBD_XML_SCHEMAS_FILE)
        if self.qbd_xml_schemas.validity != "valid":
            raise ValueError(f"QBD XML schemas are not valid: {self.qbd_xml_schemas.validity}")
        return self.qbd_xml_schemas

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapQBWC.cli()
