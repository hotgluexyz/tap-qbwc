"""Stream type classes for tap-qbwc."""

from __future__ import annotations

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
    replication_key_filter_field = "TransactionModifiedDateRangeFilter"
