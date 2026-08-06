# MySQL Setup

## Overview

The pipeline stores processed data in MySQL for analytical querying and batch-level tracking.

---

## Database Tables

### orders

Stores cleaned Bronze layer data.

Important columns

- order_id
- customer_name
- product
- price
- order_date
- batch_id
- source_file
- ingestion_timestamp

---

### orders_silver

Stores business-rule enriched Silver layer data.

Additional columns

- price_category
- discount
- final_price

---

### sales_summary

Stores aggregated Gold layer metrics.

Metrics generated

- Total Revenue
- Total Orders
- Average Order Value
- Highest Order Value
- Lowest Order Value

Each metric contains

- batch_id
- source_file
- ingestion_timestamp

---

## Batch Tracking

Each pipeline execution generates a unique Batch ID.

Example

```
BATCH_860B82C6
```

The Batch ID enables users to query records belonging to a specific execution.

Example

```sql
SELECT *
FROM orders
WHERE batch_id='BATCH_860B82C6';
```

---

## Verification

Verify the number of processed records.

```sql
SELECT COUNT(*) FROM orders;
```

```sql
SELECT COUNT(*) FROM orders_silver;
```

```sql
SELECT COUNT(*) FROM sales_summary;
```

---

## Result

All processed records remain traceable using

- Batch ID
- Source File
- Ingestion Timestamp