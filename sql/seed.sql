COPY customers FROM 'data/synthetic/customers.csv' (HEADER, DELIMITER ',');
COPY products FROM 'data/synthetic/products.csv' (HEADER, DELIMITER ',');
COPY orders FROM 'data/synthetic/orders.csv' (HEADER, DELIMITER ',');
COPY order_items FROM 'data/synthetic/order_items.csv' (HEADER, DELIMITER ',');
COPY events FROM 'data/synthetic/events.csv' (HEADER, DELIMITER ',');
COPY marketing_experiments FROM 'data/synthetic/marketing_experiments.csv' (HEADER, DELIMITER ',');
