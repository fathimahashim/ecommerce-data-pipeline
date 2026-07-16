import pandas as pd
from sqlalchemy import create_engine

# Connection to our pipeline Postgres (note port 5433)
engine = create_engine('postgresql://pipeline_user:pipeline_pass@postgres:5432/ecommerce')

def load_raw_tables():
    customers_df = pd.read_csv('data/customers.csv')
    products_df = pd.read_csv('data/products.csv')
    orders_df = pd.read_csv('data/orders.csv')

    customers_df.to_sql('raw_customers', engine, if_exists='replace', index=False)
    products_df.to_sql('raw_products', engine, if_exists='replace', index=False)
    orders_df.to_sql('raw_orders', engine, if_exists='replace', index=False)

    print(f"Loaded {len(customers_df)} rows into raw_customers")
    print(f"Loaded {len(products_df)} rows into raw_products")
    print(f"Loaded {len(orders_df)} rows into raw_orders")

if __name__ == '__main__':
    load_raw_tables()