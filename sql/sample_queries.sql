USE retail_db;

-- View Bronze table
SELECT * FROM orders;

-- View Silver table
SELECT * FROM orders_silver;

-- View Gold table
SELECT * FROM sales_summary;

-- View records from one batch
SELECT *
FROM orders
WHERE batch_id = 'BATCH_14AC12CE';

-- Count records per batch
SELECT
batch_id,
COUNT(*) AS total_records
FROM orders
GROUP BY batch_id;

-- Total revenue
SELECT
SUM(final_price) AS total_revenue
FROM orders_silver;

-- Orders by price category
SELECT
price_category,
COUNT(*)
FROM orders_silver
GROUP BY price_category;

-- Highest final price
SELECT MAX(final_price)
FROM orders_silver;

-- Lowest final price
SELECT MIN(final_price)
FROM orders_silver;

-- Gold summary
SELECT *
FROM sales_summary;