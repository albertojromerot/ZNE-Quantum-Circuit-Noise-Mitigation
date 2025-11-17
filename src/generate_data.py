import os

import numpy as np
import pandas as pd
from faker import Faker

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'synthetic')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'schema.sql')
SEED_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'seed.sql')

np.random.seed(42)
fake = Faker()
Faker.seed(42)

END_DATE = pd.Timestamp('2024-12-31')
START_DATE = END_DATE - pd.DateOffset(months=24)

COUNTRIES = ['US', 'CA', 'UK', 'DE', 'FR', 'AU', 'BR']
CHANNELS = ['organic', 'paid_search', 'social', 'email', 'referral']
EVENT_TYPES = ['visit', 'signup', 'trial_start', 'purchase', 'cancel']
CATEGORIES = ['electronics', 'apparel', 'home', 'beauty', 'outdoors', 'toys']
AGE_BANDS = ['18-24', '25-34', '35-44', '45-54', '55+']
INCOME_BANDS = ['<50k', '50-100k', '100-150k', '150k+']


def ensure_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def random_dates(n, start, end, weekly_seasonality=False):
    days = (end - start).days
    base = start + pd.to_timedelta(np.random.randint(0, days, size=n), unit='D')
    if weekly_seasonality:
        weekday = base.dt.weekday
        bump = 1 + 0.3 * np.sin(2 * np.pi * weekday / 7)
        jitter = np.random.exponential(scale=bump)
        base = base + pd.to_timedelta(jitter, unit='D')
    time_of_day = pd.to_timedelta(np.random.randint(0, 24 * 60 * 60, size=n), unit='s')
    return base + time_of_day


def generate_customers(n=50000):
    signup_dates = START_DATE + pd.to_timedelta(np.random.randint(0, (END_DATE - START_DATE).days, size=n), unit='D')
    customers = pd.DataFrame({
        'customer_id': np.arange(1, n + 1),
        'signup_date': signup_dates,
        'country': np.random.choice(COUNTRIES, size=n, p=[0.4,0.1,0.15,0.1,0.1,0.1,0.05]),
        'age_band': np.random.choice(AGE_BANDS, size=n, p=[0.15,0.3,0.25,0.2,0.1]),
        'income_band': np.random.choice(INCOME_BANDS, size=n, p=[0.25,0.4,0.25,0.1]),
        'channel': np.random.choice(CHANNELS, size=n)
    })
    return customers


def generate_products(n=50):
    prices = np.random.uniform(10, 250, size=n).round(2)
    categories = np.random.choice(CATEGORIES, size=n)
    products = pd.DataFrame({
        'product_id': np.arange(1, n + 1),
        'category': categories,
        'price_usd': prices
    })
    return products


def generate_orders(customers, products, target_orders=80000):
    customer_ids = customers['customer_id'].values
    num_orders = target_orders
    order_customers = np.random.choice(customer_ids, size=num_orders)

    order_ts = random_dates(num_orders, START_DATE, END_DATE, weekly_seasonality=True)
    revenue_usd = np.random.gamma(shape=4.0, scale=40.0, size=num_orders).round(2)
    sources = np.random.choice(['web', 'ios', 'android'], size=num_orders, p=[0.5,0.25,0.25])
    orders = pd.DataFrame({
        'order_id': np.arange(1, num_orders + 1),
        'customer_id': order_customers,
        'order_ts': order_ts,
        'revenue_usd': revenue_usd,
        'source': sources
    })

    # order items
    items = []
    for oid, cid, rev in orders[['order_id', 'customer_id', 'revenue_usd']].itertuples(index=False):
        num_items = np.random.randint(1, 4)
        chosen_products = np.random.choice(products['product_id'], size=num_items)
        qty = np.random.randint(1, 4, size=num_items)
        unit_prices = products.set_index('product_id').loc[chosen_products, 'price_usd'].values
        for pid, q, up in zip(chosen_products, qty, unit_prices):
            items.append((oid, pid, int(q), float(up)))
    order_items = pd.DataFrame(items, columns=['order_id', 'product_id', 'qty', 'unit_price_usd'])
    return orders, order_items


def generate_events(customers, target_events=200000):
    num_events = target_events
    customer_ids = np.random.choice(customers['customer_id'], size=num_events)
    event_ts = random_dates(num_events, START_DATE, END_DATE, weekly_seasonality=True)
    event_type = np.random.choice(EVENT_TYPES, size=num_events, p=[0.45,0.2,0.1,0.15,0.1])
    events = pd.DataFrame({
        'event_id': np.arange(1, num_events + 1),
        'customer_id': customer_ids,
        'event_ts': event_ts,
        'event_type': event_type
    })
    return events


def generate_marketing_experiments(customers, conversion_base=0.12, lift=0.08):
    sample_size = int(len(customers) * 0.3)
    user_ids = np.random.choice(customers['customer_id'], size=sample_size, replace=False)
    groups = np.random.choice(['A', 'B'], size=sample_size)
    exposed_ts = random_dates(sample_size, START_DATE + pd.DateOffset(months=6), END_DATE)
    converted = []
    conversion_ts = []
    for g in groups:
        prob = conversion_base * (1 + lift if g == 'B' else 1)
        c = np.random.rand() < prob
        converted.append(c)
        if c:
            delta_days = np.random.exponential(scale=5)
            conversion_ts.append(pd.Timestamp(exposed_ts[len(converted)-1]) + pd.to_timedelta(delta_days, unit='D'))
        else:
            conversion_ts.append(pd.NaT)
    exp = pd.DataFrame({
        'exp_id': np.arange(1, sample_size + 1),
        'user_id': user_ids,
        'group': groups,
        'exposed_ts': exposed_ts,
        'converted': converted,
        'conversion_ts': conversion_ts
    })
    return exp


def write_schema_and_seed():
    schema_sql = f"""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        signup_date TIMESTAMP,
        country VARCHAR,
        age_band VARCHAR,
        income_band VARCHAR,
        channel VARCHAR
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        category VARCHAR,
        price_usd DOUBLE
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_ts TIMESTAMP,
        revenue_usd DOUBLE,
        source VARCHAR
    );

    CREATE TABLE order_items (
        order_id INTEGER,
        product_id INTEGER,
        qty INTEGER,
        unit_price_usd DOUBLE
    );

    CREATE TABLE events (
        event_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        event_ts TIMESTAMP,
        event_type VARCHAR
    );

    CREATE TABLE marketing_experiments (
        exp_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        group VARCHAR,
        exposed_ts TIMESTAMP,
        converted BOOLEAN,
        conversion_ts TIMESTAMP
    );
    """
    with open(SCHEMA_PATH, 'w') as f:
        f.write(schema_sql)

    seed_sql = """
    COPY customers FROM 'data/synthetic/customers.csv' (HEADER, DELIMITER ',');
    COPY products FROM 'data/synthetic/products.csv' (HEADER, DELIMITER ',');
    COPY orders FROM 'data/synthetic/orders.csv' (HEADER, DELIMITER ',');
    COPY order_items FROM 'data/synthetic/order_items.csv' (HEADER, DELIMITER ',');
    COPY events FROM 'data/synthetic/events.csv' (HEADER, DELIMITER ',');
    COPY marketing_experiments FROM 'data/synthetic/marketing_experiments.csv' (HEADER, DELIMITER ',');
    """
    with open(SEED_PATH, 'w') as f:
        f.write(seed_sql)


def main():
    ensure_output()
    customers = generate_customers()
    products = generate_products()
    orders, order_items = generate_orders(customers, products)
    events = generate_events(customers)
    experiments = generate_marketing_experiments(customers)

    customers.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
    products.to_csv(os.path.join(OUTPUT_DIR, 'products.csv'), index=False)
    orders.to_csv(os.path.join(OUTPUT_DIR, 'orders.csv'), index=False)
    order_items.to_csv(os.path.join(OUTPUT_DIR, 'order_items.csv'), index=False)
    events.to_csv(os.path.join(OUTPUT_DIR, 'events.csv'), index=False)
    experiments.to_csv(os.path.join(OUTPUT_DIR, 'marketing_experiments.csv'), index=False)

    write_schema_and_seed()
    print('Synthetic data written to', OUTPUT_DIR)


if __name__ == '__main__':
    main()
