import os
import pandas as pd

from airflow.models import Variable
from airflow.providers.mysql.hooks.mysql import MySqlHook

from config.config import (
    BRONZE_DATA_PATH,
    SILVER_DATA_PATH,
    GOLD_DATA_PATH,
)


# ---------------------------------------------------------
# Airflow Variable
# ---------------------------------------------------------

PROJECT_PATH = Variable.get("PROJECT_PATH")


# ---------------------------------------------------------
# Build absolute paths
# ---------------------------------------------------------

BRONZE_FILE_PATH = os.path.join(
    PROJECT_PATH,
    BRONZE_DATA_PATH
)

SILVER_FILE_PATH = os.path.join(
    PROJECT_PATH,
    SILVER_DATA_PATH
)

GOLD_FILE_PATH = os.path.join(
    PROJECT_PATH,
    GOLD_DATA_PATH
)


# ---------------------------------------------------------
# Bronze → MySQL
# ---------------------------------------------------------

def load_orders():

    print("Starting Bronze to MySQL loading")

    print(f"Reading Bronze file from: {BRONZE_FILE_PATH}")

    df = pd.read_csv(BRONZE_FILE_PATH)

    print(f"Bronze records found: {len(df)}")

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()

    query = """
    INSERT INTO orders
    (
        order_id,
        customer_name,
        product,
        price,
        order_date
    )
    VALUES (%s,%s,%s,%s,%s)

    ON DUPLICATE KEY UPDATE

    customer_name = VALUES(customer_name),
    product = VALUES(product),
    price = VALUES(price),
    order_date = VALUES(order_date)
    """

    data = []

    for _, row in df.iterrows():

        data.append(
            (
                row["order_id"],
                row["customer_name"],
                row["product"],
                row["price"],
                row["order_date"],
            )
        )

    cursor.executemany(
        query,
        data
    )

    connection.commit()

    print(
        f"Successfully loaded {len(data)} Bronze records into MySQL"
    )

    cursor.close()
    connection.close()


# ---------------------------------------------------------
# Silver → MySQL
# ---------------------------------------------------------

def load_silver():

    print("Starting Silver to MySQL loading")

    print(f"Reading Silver file from: {SILVER_FILE_PATH}")

    df = pd.read_csv(SILVER_FILE_PATH)

    print(f"Silver records found: {len(df)}")

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()

    query = """
    INSERT INTO orders_silver
    (
        order_id,
        customer_name,
        product,
        price,
        order_date,
        price_category,
        discount,
        final_price
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

    ON DUPLICATE KEY UPDATE

    customer_name = VALUES(customer_name),
    product = VALUES(product),
    price = VALUES(price),
    order_date = VALUES(order_date),
    price_category = VALUES(price_category),
    discount = VALUES(discount),
    final_price = VALUES(final_price)
    """

    data = []

    for _, row in df.iterrows():

        data.append(
            (
                row["order_id"],
                row["customer_name"],
                row["product"],
                row["price"],
                row["order_date"],
                row["price_category"],
                row["discount"],
                row["final_price"],
            )
        )

    cursor.executemany(
        query,
        data
    )

    connection.commit()

    print(
        f"Successfully loaded {len(data)} Silver records into MySQL"
    )

    cursor.close()
    connection.close()


# ---------------------------------------------------------
# Gold → MySQL
# ---------------------------------------------------------

def load_sales_summary():

    print("Starting Gold to MySQL loading")

    print(f"Reading Gold file from: {GOLD_FILE_PATH}")

    df = pd.read_csv(GOLD_FILE_PATH)

    print(f"Gold records found: {len(df)}")

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()

    query = """
    INSERT INTO sales_summary
    (
        metric,
        value
    )
    VALUES (%s,%s)

    ON DUPLICATE KEY UPDATE

    value = VALUES(value)
    """

    data = []

    for _, row in df.iterrows():

        data.append(
            (
                row["metric"],
                row["value"]
            )
        )

    cursor.executemany(
        query,
        data
    )

    connection.commit()

    print(
        f"Successfully loaded {len(data)} Gold records into MySQL"
    )

    cursor.close()
    connection.close()