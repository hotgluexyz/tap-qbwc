"""Stream type classes for tap-qbwc."""

from __future__ import annotations

from tap_qbwc.base_stream import QBWCDynamicSchemaStream


class AccountsStream(QBWCDynamicSchemaStream):
    """Stream for ``accounts``."""

    name = "accounts"
    response_element = "AccountQueryRs"
    request_element = "AccountQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for accounts because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class ClassesStream(QBWCDynamicSchemaStream):
    """Stream for ``classes``."""

    name = "classes"
    response_element = "ClassQueryRs"
    request_element = "ClassQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for classes because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class CustomersStream(QBWCDynamicSchemaStream):
    """Stream for ``customers``."""

    name = "customers"
    response_element = "CustomerQueryRs"
    request_element = "CustomerQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class VendorsStream(QBWCDynamicSchemaStream):
    """Stream for ``vendors``."""

    name = "vendors"
    response_element = "VendorQueryRs"
    request_element = "VendorQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class ItemsStream(QBWCDynamicSchemaStream):
    """Stream for ``items``."""

    name = "items"
    response_element = "ItemQueryRs"
    request_element = "ItemQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class InventoryItemsStream(QBWCDynamicSchemaStream):
    """Stream for ``inventory_items``."""

    name = "inventory_items"
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
    """Stream for ``price_levels``."""

    name = "price_levels"
    response_element = "PriceLevelQueryRs"
    request_element = "PriceLevelQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for price levels because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class UnitOfMeasureSetsStream(QBWCDynamicSchemaStream):
    """Stream for ``unit_of_measure_sets``."""

    name = "unit_of_measure_sets"
    response_element = "UnitOfMeasureSetQueryRs"
    request_element = "UnitOfMeasureSetQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for unit of measure sets because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class SalesTaxCodesStream(QBWCDynamicSchemaStream):
    """Stream for ``sales_tax_codes``."""

    name = "sales_tax_codes"
    response_element = "SalesTaxCodeQueryRs"
    request_element = "SalesTaxCodeQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"
    # use a high page size for sales tax codes because it doesn't support pagination
    page_size = 5000
    should_paginate = False


class ItemSalesTaxesStream(QBWCDynamicSchemaStream):
    """Stream for ``item_sales_taxes``."""

    name = "item_sales_taxes"
    response_element = "ItemSalesTaxQueryRs"
    request_element = "ItemSalesTaxQueryRq"
    primary_keys = ["ListID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "FromModifiedDate"


class BillsStream(QBWCDynamicSchemaStream):
    """Stream for ``bills``."""

    name = "bills"
    response_element = "BillQueryRs"
    request_element = "BillQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class BillPaymentsCheckStream(QBWCDynamicSchemaStream):
    """Stream for ``bill_payments_check``."""

    name = "bill_payments_check"
    response_element = "BillPaymentCheckQueryRs"
    request_element = "BillPaymentCheckQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class BillPaymentsCreditCardStream(QBWCDynamicSchemaStream):
    """Stream for ``bill_payments_credit_card``."""

    name = "bill_payments_credit_card"
    response_element = "BillPaymentCreditCardQueryRs"
    request_element = "BillPaymentCreditCardQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class InvoicesStream(QBWCDynamicSchemaStream):
    """Stream for ``invoices``."""

    name = "invoices"
    response_element = "InvoiceQueryRs"
    request_element = "InvoiceQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class PurchaseOrdersStream(QBWCDynamicSchemaStream):
    """Stream for ``purchase_orders``."""

    name = "purchase_orders"
    response_element = "PurchaseOrderQueryRs"
    request_element = "PurchaseOrderQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class CreditMemosStream(QBWCDynamicSchemaStream):
    """Stream for ``credit_memos``."""

    name = "credit_memos"
    response_element = "CreditMemoQueryRs"
    request_element = "CreditMemoQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class SalesOrdersStream(QBWCDynamicSchemaStream):
    """Stream for ``sales_orders``."""

    name = "sales_orders"
    response_element = "SalesOrderQueryRs"
    request_element = "SalesOrderQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class SalesReceiptsStream(QBWCDynamicSchemaStream):
    """Stream for ``sales_receipts``."""

    name = "sales_receipts"
    response_element = "SalesReceiptQueryRs"
    request_element = "SalesReceiptQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class VendorCreditsStream(QBWCDynamicSchemaStream):
    """Stream for ``vendor_credits``."""

    name = "vendor_credits"
    response_element = "VendorCreditQueryRs"
    request_element = "VendorCreditQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class EstimatesStream(QBWCDynamicSchemaStream):
    """Stream for ``estimates``."""

    name = "estimates"
    response_element = "EstimateQueryRs"
    request_element = "EstimateQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class JournalEntriesStream(QBWCDynamicSchemaStream):
    """Stream for ``journal_entries``."""

    name = "journal_entries"
    response_element = "JournalEntryQueryRs"
    request_element = "JournalEntryQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True


class ChecksStream(QBWCDynamicSchemaStream):
    """Stream for ``checks``."""

    name = "checks"
    response_element = "CheckQueryRs"
    request_element = "CheckQueryRq"
    primary_keys = ["TxnID"]
    replication_key = "TimeModified"
    replication_key_filter_field = "ModifiedDateRangeFilter"
    include_line_items = True
