# E-Commerce Sales Analytics Pipeline

An automated ETL pipeline that transforms raw e-commerce order data into an analytics-ready star schema, orchestrated with Apache Airflow.

## Architecture

```
Raw data (customers, products, orders)
        ↓
[Airflow DAG - scheduled daily]
        ↓
Extract & Load Raw → Validate Raw Data → Transform to Star Schema → Validate Star Schema
        ↓
Postgres warehouse (fact + dimension tables)
```

## Tech Stack

- **Python** (Pandas, SQLAlchemy) — extraction and transformation logic
- **PostgreSQL** — source data and warehouse storage
- **Apache Airflow** — orchestration, scheduling, retries
- **Docker Compose** — local infrastructure (Postgres + Airflow, isolated services for webserver/scheduler)

## Data Model

Star schema design:

- `orders_fact` — one row per order line (customer_key, product_key, date_key, quantity, revenue)
- `customer_dim`, `product_dim`, `date_dim` — descriptive dimension tables

This design was chosen over the normalized source schema specifically to make analytical queries (revenue by region, by quarter, by category) simple joins instead of multi-table traversals.

## Pipeline Stages

1. **extract_load_raw** — loads raw CSV data into staging tables (simulates pulling from a live app database)
2. **validate_raw** — checks for duplicates, nulls, and invalid values before transformation
3. **transform_star_schema** — builds fact and dimension tables from raw data
4. **validate_fact** — checks the transformed data for integrity before it's considered "ready"

Each stage is a separate Airflow task with independent retry logic, so failures are isolated and traceable rather than crashing the whole pipeline silently.

## Running Locally

```bash
docker compose up -d
# Airflow UI: http://localhost:8080 (admin/admin)
# Trigger the 'ecommerce_sales_pipeline' DAG manually or let it run on its @daily schedule
```

## Example Query

```sql
SELECT c.state, d.quarter, SUM(f.revenue) AS total_revenue
FROM orders_fact f
JOIN customer_dim c ON f.customer_key = c.customer_key
JOIN date_dim d ON f.date_key = d.date_key
GROUP BY c.state, d.quarter
ORDER BY total_revenue DESC;
```

## Design Decisions

- **Idempotent loads**: transformation tables use `if_exists='replace'` at this stage to keep the demo simple; a production version would use incremental upserts keyed on `order_id`.
- **Validation gates**: data quality checks run _between_ pipeline stages, not just at the end, so bad data never reaches the final warehouse tables.
- **Separated webserver/scheduler**: Airflow services are split into independent containers rather than one combined process, matching how Airflow is typically deployed in production.
