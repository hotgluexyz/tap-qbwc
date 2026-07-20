# tap-qbwc

A [Singer](https://www.singer.io/) tap that extracts **QuickBooks Desktop** data via the [Hotglue QBWC](https://docs.hotglue.com) HTTP bridge. It is built with [hotglue-singer-sdk](https://github.com/hotgluexyz/HotglueSingerSDK) and speaks the standard Singer message protocol on stdout, so you can pair it with any compatible target.

## Features

- Talks to QuickBooks Desktop through Hotglue QBWC: authenticate with a Bearer token, send qbXML requests, and poll for responses.
- Uses **qbXML 13.0** and builds stream schemas dynamically from the bundled QBD XSD (`tap_qbwc/qbd_xml_schemas`).
- Incremental sync on `TimeModified` (bookmark + optional `start_date`), except full-table `item_sites`.
- Iterator-based pagination (default page size 200). Some list streams that do not support iterators use a single large page (`page_size=5000`).

### Streams

| Stream | qbXML query | Primary key | Replication key | Notes |
| ------ | ----------- | ----------- | ----------------- | ----- |
| `accounts` | `AccountQueryRq` | `ListID` | `TimeModified` | No iterator; `page_size=5000` |
| `classes` | `ClassQueryRq` | `ListID` | `TimeModified` | No iterator; `page_size=5000` |
| `customers` | `CustomerQueryRq` | `ListID` | `TimeModified` | Paginated |
| `vendors` | `VendorQueryRq` | `ListID` | `TimeModified` | Paginated |
| `items` | `ItemQueryRq` | `ListID` | `TimeModified` | Merges multiple `*Ret` types; adds `ItemType` |
| `inventory_items` | `ItemInventoryQueryRq` | `ListID` | `TimeModified` | Paginated |
| `item_sites` | `ItemSitesQueryRq` | `ListID` | — | Full table |
| `price_levels` | `PriceLevelQueryRq` | `ListID` | `TimeModified` | No iterator; `page_size=5000` |
| `unit_of_measure_sets` | `UnitOfMeasureSetQueryRq` | `ListID` | `TimeModified` | No iterator; `page_size=5000` |
| `sales_tax_codes` | `SalesTaxCodeQueryRq` | `ListID` | `TimeModified` | No iterator; `page_size=5000` |
| `item_sales_taxes` | `ItemSalesTaxQueryRq` | `ListID` | `TimeModified` | Paginated |
| `bills` | `BillQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `bill_payments_check` | `BillPaymentCheckQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `bill_payments_credit_card` | `BillPaymentCreditCardQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `invoices` | `InvoiceQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `purchase_orders` | `PurchaseOrderQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `credit_memos` | `CreditMemoQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `sales_orders` | `SalesOrderQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `sales_receipts` | `SalesReceiptQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `vendor_credits` | `VendorCreditQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `estimates` | `EstimateQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `journal_entries` | `JournalEntryQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `checks` | `CheckQueryRq` | `TxnID` | `TimeModified` | Includes line items |
| `transactions` | `TransactionQueryRq` | `TxnID` | `TimeModified` | Uses `TransactionModifiedDateRangeFilter` |

**Incremental filters:** list streams use `FromModifiedDate`; most transaction streams use `ModifiedDateRangeFilter` / `FromModifiedDate`; `transactions` uses `TransactionModifiedDateRangeFilter`. Selected catalog properties are passed as `IncludeRetElement`. Transaction streams listed above also set `IncludeLineItems=true`.

## Requirements

- Python **3.10+** (see `requires-python` in `pyproject.toml`).
- A working Hotglue QBWC / QuickBooks Desktop Web Connector setup and a Hotglue-issued `token`.

## Installation

1. **Clone** this repository and `cd` into the project directory.
2. **Create `config.json`** in the project root with your credentials and settings (see [Configuration](#configuration) for the fields and an example).
3. **Create a virtual environment** and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

4. **Install the package** in editable mode:

```bash
pip install -e .
```

5. **Run the tap** (with the venv still activated):

```bash
tap-qbwc --help
```

## Configuration

| Setting | Type | Required | Default | Description |
| ------- | ---- | -------- | ------- | ----------- |
| `token` | string | yes | — | Bearer token used to authenticate with the Hotglue QBWC API (**sensitive**). |
| `start_date` | string (datetime) | no | `2000-01-01T00:00:00Z` | Earliest `TimeModified` to sync on incremental streams. |
| `request_timeout` | integer | no | `1800` | How long to wait for a QBWC request to complete, in seconds. |
| `qbwc_is_alive_timeout` | integer | no | `3600` | How long to wait for the QBWC host ping (`HostQueryRq`) to complete, in seconds. |
| `is_sandbox` | boolean | no | `false` | When `true`, use the sandbox QBWC host instead of production. |

Run `tap-qbwc --about` (or `tap-qbwc --about --format=markdown`) for the authoritative schema for your installed version.

### Example `config.json`

```json
{
  "token": "YOUR_HOTGLUE_QBWC_TOKEN",
  "start_date": "2000-01-01T00:00:00Z",
  "request_timeout": 1800,
  "qbwc_is_alive_timeout": 3600,
  "is_sandbox": false
}
```

Do not commit real credentials. Prefer environment variables or a secrets manager in production.

### Environment-based config

You can load settings from the process environment using `--config=ENV` (the SDK merges env into config). Env names follow the tap’s setting keys (for example `TAP_QBWC_TOKEN`); see `tap-qbwc --about`.

## Usage

With your virtual environment **activated** and `config.json` in place:

Discover stream catalog:

```bash
tap-qbwc --config config.json --discover > catalog.json
```

Run a sync (with optional state):

```bash
tap-qbwc --config config.json --catalog catalog.json --state state.json
```

Pipe to any Singer target:

```bash
tap-qbwc --config config.json --catalog catalog.json | target-jsonl
```

Inspect built-in settings and stream metadata:

```bash
tap-qbwc --about
```

## API / documentation

Hotglue QBWC hosts (selected by `is_sandbox`):

| Environment | Base URL |
| ----------- | -------- |
| Production | `https://qbwc.hotglue.com` |
| Sandbox | `https://qbwc-qa.hotglue.xyz` |

Request flow:

1. `POST /authenticate` with `Authorization: Bearer <token>` → `session_id`
2. Ping the desktop host with a `HostQueryRq` (uses `qbwc_is_alive_timeout`)
3. `POST /send_qbwc_request?session_id=…` with qbXML payload → `request_id`
4. Poll `GET /get_qbwc_response?session_id=…&request_id=…` until completed, error, or timeout

See [Hotglue documentation](https://docs.hotglue.com) for connector setup and token issuance.

## License

Apache 2.0 — see `LICENSE` and `pyproject.toml`.
