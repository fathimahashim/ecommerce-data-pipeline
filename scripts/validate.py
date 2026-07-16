import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://pipeline_user:pipeline_pass@postgres:5432/ecommerce')

def validate_raw_orders():
    df = pd.read_sql('SELECT * FROM raw_orders', engine)
    errors = []

    if df.empty:
        errors.append("raw_orders is empty")

    if df['order_id'].duplicated().any():
        errors.append(f"Found {df['order_id'].duplicated().sum()} duplicate order_ids")

    if df['customer_id'].isnull().any():
        errors.append(f"Found {df['customer_id'].isnull().sum()} rows with missing customer_id")

    if (df['quantity'] <= 0).any():
        errors.append("Found rows with zero or negative quantity")

    if errors:
        raise ValueError("Data validation failed:\n" + "\n".join(errors))

    print(f"Validation passed: {len(df)} rows in raw_orders")
    return True

def validate_star_schema():
    fact_df = pd.read_sql('SELECT * FROM orders_fact', engine)
    errors = []

    if fact_df['revenue'].isnull().any():
        errors.append("Found null revenue values in orders_fact")

    if (fact_df['revenue'] < 0).any():
        errors.append("Found negative revenue values in orders_fact")

    if errors:
        raise ValueError("Star schema validation failed:\n" + "\n".join(errors))

    print(f"Validation passed: {len(fact_df)} rows in orders_fact")
    return True

if __name__ == '__main__':
    validate_raw_orders()
    validate_star_schema()