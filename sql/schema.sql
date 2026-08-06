mysql> select * from orders;
+----------+---------------+------------+----------+------------+----------------+---------------------------------------+---------------------+
| order_id | customer_name | product    | price    | order_date | batch_id       | source_file                           | ingestion_timestamp |
+----------+---------------+------------+----------+------------+----------------+---------------------------------------+---------------------+
|     1001 | Kiran         | Mouse      |  1200.00 | 2026-07-01 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1002 | Meera         | Headphones |  3500.00 | 2026-07-08 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1003 | Diana         | Keyboard   |  2500.00 | 2026-07-24 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1004 | Bob           | Mouse      |  1200.00 | 2026-07-19 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1005 | Grace         | Laptop     | 75000.00 | 2026-07-01 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1006 | Bob           | Monitor    | 15000.00 | 2026-07-08 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1007 | Ivy           | Laptop     | 75000.00 | 2026-07-18 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1008 | Diana         | Printer    | 12000.00 | 2026-07-08 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |



mysql> select * from orders_silver;
+----------+---------------+------------+----------+------------+----------------+----------+-------------+----------------+---------------------------------------+---------------------+
| order_id | customer_name | product    | price    | order_date | price_category | discount | final_price | batch_id       | source_file                           | ingestion_timestamp |
+----------+---------------+------------+----------+------------+----------------+----------+-------------+----------------+---------------------------------------+---------------------+
|     1001 | Kiran         | Mouse      |  1200.00 | 2026-07-01 | Low            |     5.00 |     1140.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1002 | Meera         | Headphones |  3500.00 | 2026-07-08 | Low            |     5.00 |     3325.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1003 | Diana         | Keyboard   |  2500.00 | 2026-07-24 | Low            |     5.00 |     2375.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1004 | Bob           | Mouse      |  1200.00 | 2026-07-19 | Low            |     5.00 |     1140.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|     1005 | Grace         | Laptop     | 75000.00 | 2026-07-01 | High           |    15.00 |    63750.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |


mysql> select * from sales_summary;
+----+---------------------+-----------+----------------+---------------------------------------+---------------------+
| id | metric              | value     | batch_id       | source_file                           | ingestion_timestamp |
+----+---------------------+-----------+----------------+---------------------------------------+---------------------+
|  1 | Total Revenue       | 879025.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|  2 | Total Orders        |     55.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|  3 | Average Order Value |  15982.27 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|  4 | Highest Order Value |  63750.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
|  5 | Lowest Order Value  |   1140.00 | BATCH_14AC12CE | external_orders_messy_110_records.csv | 2026-08-06 13:50:22 |
