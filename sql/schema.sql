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
