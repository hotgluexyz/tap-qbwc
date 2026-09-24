"""Stream type classes for tap-qbwc."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from typing_extensions import override

from tap_qbwc.base_stream import QBWCDynamicSchemaStream


class AccountsStream(QBWCDynamicSchemaStream):
    """Stream for ``account``."""

    name = "account"
    response_element = "AccountQueryRs"
    request_element = "AccountQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for accounts because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class ClassesStream(QBWCDynamicSchemaStream):
    """Stream for ``class``."""

    name = "class"
    response_element = "ClassQueryRs"
    request_element = "ClassQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for classes because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class CustomersStream(QBWCDynamicSchemaStream):
    """Stream for ``customer``."""

    name = "customer"
    response_element = "CustomerQueryRs"
    request_element = "CustomerQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class VendorsStream(QBWCDynamicSchemaStream):
    """Stream for ``vendor``."""

    name = "vendor"
    response_element = "VendorQueryRs"
    request_element = "VendorQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class ItemsStream(QBWCDynamicSchemaStream):
    """Stream for ``item``."""

    name = "item"
    response_element = "ItemQueryRs"
    request_element = "ItemQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class InventoryItemsStream(QBWCDynamicSchemaStream):
    """Stream for ``inventory_item``."""

    name = "inventory_item"
    response_element = "ItemInventoryQueryRs"
    request_element = "ItemInventoryQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class ItemSitesStream(QBWCDynamicSchemaStream):
    """Stream for ``item_sites``."""

    name = "item_sites"
    response_element = "ItemSitesQueryRs"
    request_element = "ItemSitesQueryRq"
    primary_keys = ["ListID"]
    replication_key = None
    replication_key_filter_field = None


class PriceLevelsStream(QBWCDynamicSchemaStream):
    """Stream for ``price_level``."""

    name = "price_level"
    response_element = "PriceLevelQueryRs"
    request_element = "PriceLevelQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for price levels because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class UnitOfMeasureSetsStream(QBWCDynamicSchemaStream):
    """Stream for ``unit_of_measure_set``."""

    name = "unit_of_measure_set"
    response_element = "UnitOfMeasureSetQueryRs"
    request_element = "UnitOfMeasureSetQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for unit of measure sets because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class SalesTaxCodesStream(QBWCDynamicSchemaStream):
    """Stream for ``sales_tax_code``."""

    name = "sales_tax_code"
    response_element = "SalesTaxCodeQueryRs"
    request_element = "SalesTaxCodeQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for sales tax codes because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class ItemSalesTaxesStream(QBWCDynamicSchemaStream):
    """Stream for ``item_sales_tax``."""

    name = "item_sales_tax"
    response_element = "ItemSalesTaxQueryRs"
    request_element = "ItemSalesTaxQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class BillsStream(QBWCDynamicSchemaStream):
    """Stream for ``bill``."""

    name = "bill"
    response_element = "BillQueryRs"
    request_element = "BillQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class BillPaymentsCheckStream(QBWCDynamicSchemaStream):
    """Stream for ``bill_payment_check``."""

    name = "bill_payment_check"
    response_element = "BillPaymentCheckQueryRs"
    request_element = "BillPaymentCheckQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class BillPaymentsCreditCardStream(QBWCDynamicSchemaStream):
    """Stream for ``bill_payment_credit_card``."""

    name = "bill_payment_credit_card"
    response_element = "BillPaymentCreditCardQueryRs"
    request_element = "BillPaymentCreditCardQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class InvoicesStream(QBWCDynamicSchemaStream):
    """Stream for ``invoice``."""

    name = "invoice"
    response_element = "InvoiceQueryRs"
    request_element = "InvoiceQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class PurchaseOrdersStream(QBWCDynamicSchemaStream):
    """Stream for ``purchase_order``."""

    name = "purchase_order"
    response_element = "PurchaseOrderQueryRs"
    request_element = "PurchaseOrderQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class CreditMemosStream(QBWCDynamicSchemaStream):
    """Stream for ``credit_memo``."""

    name = "credit_memo"
    response_element = "CreditMemoQueryRs"
    request_element = "CreditMemoQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class SalesOrdersStream(QBWCDynamicSchemaStream):
    """Stream for ``sale_order``."""

    name = "sale_order"
    response_element = "SalesOrderQueryRs"
    request_element = "SalesOrderQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class SalesReceiptsStream(QBWCDynamicSchemaStream):
    """Stream for ``sales_receipt``."""

    name = "sales_receipt"
    response_element = "SalesReceiptQueryRs"
    request_element = "SalesReceiptQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class VendorCreditsStream(QBWCDynamicSchemaStream):
    """Stream for ``vendor_credit``."""

    name = "vendor_credit"
    response_element = "VendorCreditQueryRs"
    request_element = "VendorCreditQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class EstimatesStream(QBWCDynamicSchemaStream):
    """Stream for ``estimate``."""

    name = "estimate"
    response_element = "EstimateQueryRs"
    request_element = "EstimateQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class JournalEntriesStream(QBWCDynamicSchemaStream):
    """Stream for ``journal_entry``."""

    name = "journal_entry"
    response_element = "JournalEntryQueryRs"
    request_element = "JournalEntryQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class ChecksStream(QBWCDynamicSchemaStream):
    """Stream for ``check``."""

    name = "check"
    response_element = "CheckQueryRs"
    request_element = "CheckQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class TransactionsStream(QBWCDynamicSchemaStream):
    """Stream for ``transaction_list``."""

    name = "transaction_list"
    response_element = "TransactionQueryRs"
    request_element = "TransactionQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    # Transactions are filtered by transaction date (TxnDate), not TimeModified, so
    # the payload's date filter is built in ``prepare_request_payload`` below rather
    # than by the base class. ``replication_key`` stays TimeModified for state and
    # initial-sync detection.
    replication_key_filter_field = None

    def _is_initial_sync(self, context: dict | None) -> bool:
        """True on the first sync, i.e. when no bookmark newer than start_date exists."""
        bookmark = self.get_starting_timestamp(context)
        if bookmark is None:
            return True
        return bookmark == self.get_config_start_date()

    def _report_period_start_date(self, report_periods: int) -> datetime:
        """First day of the calendar month ``report_periods - 1`` months before today.

        e.g. with report_periods=3 in July, returns May 1 so the window
        [May 1 .. today] covers the current month plus the two prior months.
        """
        today = datetime.now(timezone.utc)
        month_index = today.year * 12 + (today.month - 1) - (report_periods - 1)
        start_year, start_month = divmod(month_index, 12)
        return datetime(start_year, start_month + 1, 1, tzinfo=timezone.utc)

    def prepare_request_payload(
        self, context: dict | None, iterator_id: str | None, is_count_request: bool = False
    ) -> dict | None:
        """Filter transactions by transaction date (TxnDate).

        The initial sync fetches every transaction on/after the configured
        ``start_date``. Every subsequent sync instead fetches all transactions whose
        transaction date falls in the last ``report_periods`` calendar months so the
        P&L report can be rebuilt.
        """
        payload = super().prepare_request_payload(context, iterator_id, is_count_request)

        if self._is_initial_sync(context):
            from_txn_date = self.get_starting_time(context)
        else:
            report_periods = self.config.get("report_periods", 3)
            from_txn_date = self._report_period_start_date(report_periods)
            self.logger.info(
                f"Not initial sync, fetching transactions for the last {report_periods} "
                f"months, starting from {from_txn_date.strftime('%Y-%m-%d')}"
            )

        payload[self.request_element]["TransactionDateRangeFilter"] = {
            "FromTxnDate": from_txn_date.strftime("%Y-%m-%d"),
        }
        return payload

class PreferencesStream(QBWCDynamicSchemaStream):
    """Stream for ``preference`` (company settings including ClosingDate)."""

    name = "preference"
    response_element = "PreferencesQueryRs"
    request_element = "PreferencesQueryRq"
    primary_keys = []
    replication_key = None
    replication_key_filter_field = None
    should_paginate = False

    @override
    def prepare_request_payload(
        self,
        context: dict | None,
        iterator_id: str | None,
        is_count_request: bool = False,
    ) -> dict | None:
        # PreferencesQueryRq only supports IncludeRetElement - no MaxReturned/iterator.
        request_data: dict = {}
        if self.selected_properties:
            request_data["IncludeRetElement"] = self.selected_properties
        return {self.request_element: request_data}

    @override
    def parse_response(self, response: dict) -> Iterable[dict]:
        rs_list = response.get(self.response_element) or []
        if not rs_list:
            return

        prefs = rs_list[0].get("PreferencesRet")
        if not prefs:
            return

        if isinstance(prefs, list):
            yield from prefs
        else:
            yield prefs