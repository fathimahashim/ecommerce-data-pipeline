import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

# Generate customers
def generate_customers(n=200):
    customers = []
    for i in range(1, n + 1):
        customers.append({
            'customer_id': i,
            'customer_name': fake.name(),
            'email': fake.email(),
            'city': fake.city(),
            'state': fake.state(),
            'signup_date': fake.date_between(start_date='-2y', end_date='-30d')
        })
    return pd.DataFrame(customers)

# Generate products
def generate_products(n=50):
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Toys']
    products = []
    for i in range(1, n + 1):
        products.append({
            'product_id': i,
            'product_name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'category': random.choice(categories),
            'unit_price': round(random.uniform(5, 500), 2)
        })
    return pd.DataFrame(products)

# Generate orders (this is our main "fact" source)
def generate_orders(n=3000, num_customers=200, num_products=50):
    orders = []
    start_date = datetime.now() - timedelta(days=180)
    for i in range(1, n + 1):
        order_date = start_date + timedelta(days=random.randint(0, 180))
        quantity = random.randint(1, 5)
        orders.append({
            'order_id': i,
            'customer_id': random.randint(1, num_customers),
            'product_id': random.randint(1, num_products),
            'order_date': order_date.date(),
            'quantity': quantity,
        })
    return pd.DataFrame(orders)

if __name__ == '__main__':
    customers_df = generate_customers()
    products_df = generate_products()
    orders_df = generate_orders()

    customers_df.to_csv('data/customers.csv', index=False)
    products_df.to_csv('data/products.csv', index=False)
    orders_df.to_csv('data/orders.csv', index=False)

    print(f"Generated {len(customers_df)} customers")
    print(f"Generated {len(products_df)} products")
    print(f"Generated {len(orders_df)} orders")