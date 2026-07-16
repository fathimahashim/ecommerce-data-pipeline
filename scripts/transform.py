import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://pipeline_user:pipeline_pass@postgres:5432/ecommerce')

def build_date_dim(orders_df):
    dates = pd.to_datetime(orders_df['order_date']).dt.date.unique()
    date_dim = pd.DataFrame({'full_date': dates})
    date_dim['full_date'] = pd.to_datetime(date_dim['full_date'])
    date_dim['date_key'] = date_dim['full_date'].dt.strftime('%Y%m%d').astype(int)
    date_dim['year'] = date_dim['full_date'].dt.year
    date_dim['month'] = date_dim['full_date'].dt.month
    date_dim['quarter'] = date_dim['full_date'].dt.quarter
    date_dim['day_of_week'] = date_dim['full_date'].dt.day_name()
    return date_dim[['date_key', 'full_date', 'year', 'month', 'quarter', 'day_of_week']]

def build_customer_dim(customers_df):
    customer_dim = customers_df.copy()
    customer_dim = customer_dim.rename(columns={'customer_id': 'customer_key'})
    return customer_dim

def build_product_dim(products_df):
    product_dim = products_df.copy()
    product_dim = product_dim.rename(columns={'product_id': 'product_key'})
    return product_dim

def build_orders_fact(orders_df, products_df):
    fact = orders_df.copy()
    fact = fact.merge(products_df[['product_id', 'unit_price']], on='product_id', how='left')
    fact['revenue'] = fact['quantity'] * fact['unit_price']
    fact['order_date'] = pd.to_datetime(fact['order_date'])
    fact['date_key'] = fact['order_date'].dt.strftime('%Y%m%d').astype(int)

    fact = fact.rename(columns={'customer_id': 'customer_key', 'product_id': 'product_key'})
    return fact[['order_id', 'customer_key', 'product_key', 'date_key', 'quantity', 'revenue']]

def run_transformation():
    orders_df = pd.read_sql('SELECT * FROM raw_orders', engine)
    customers_df = pd.read_sql('SELECT * FROM raw_customers', engine)
    products_df = pd.read_sql('SELECT * FROM raw_products', engine)

    date_dim = build_date_dim(orders_df)
    customer_dim = build_customer_dim(customers_df)
    product_dim = build_product_dim(products_df)
    orders_fact = build_orders_fact(orders_df, products_df)

    date_dim.to_sql('date_dim', engine, if_exists='replace', index=False)
    customer_dim.to_sql('customer_dim', engine, if_exists='replace', index=False)
    product_dim.to_sql('product_dim', engine, if_exists='replace', index=False)
    orders_fact.to_sql('orders_fact', engine, if_exists='replace', index=False)

    print(f"Built date_dim: {len(date_dim)} rows")
    print(f"Built customer_dim: {len(customer_dim)} rows")
    print(f"Built product_dim: {len(product_dim)} rows")
    print(f"Built orders_fact: {len(orders_fact)} rows")

if __name__ == '__main__':
    run_transformation()