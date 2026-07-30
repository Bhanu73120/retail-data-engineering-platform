import os
import pandas as pd

from airflow.providers.mysql.hooks.mysql import MySqlHook

from airflow.models import Variable


# ---------------------------------------------------------
# Airflow Variable
# ---------------------------------------------------------

PROJECT_PATH = Variable.get(
    "PROJECT_PATH"
)


# =========================================================
# BRONZE → MYSQL
# =========================================================

def load_orders(
    bronze_file_path
):

    print(
        "Starting Bronze to MySQL loading"
    )

    print(
        f"Reading Bronze file from: "
        f"{bronze_file_path}"
    )


    # -----------------------------------------------------
    # Read Bronze File
    # -----------------------------------------------------

    df = pd.read_csv(
        bronze_file_path
    )

    batch_id = df["batch_id"].iloc[0]
    print(
        f"Batch ID: "
        f"{batch_id}"
    )

    bronze_count = len(
        df
    )

    print(
        f"Bronze records found: "
        f"{bronze_count}"
    )


    # -----------------------------------------------------
    # MySQL Connection
    # -----------------------------------------------------

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Insert Bronze Data
    # -----------------------------------------------------

    query = """

    INSERT INTO orders
    (
        order_id,
        customer_name,
        product,
        price,
        order_date,
        batch_id
    )

    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )

    ON DUPLICATE KEY UPDATE

    customer_name = VALUES(customer_name),
    product = VALUES(product),
    price = VALUES(price),
    order_date = VALUES(order_date),
    batch_id = VALUES(batch_id)

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
                row["batch_id"],
            )
        )


    cursor.executemany(
        query,
        data
    )

    connection.commit()


    print(
        f"Successfully loaded "
        f"{len(data)} Bronze records "
        f"into MySQL"
    )


    # -----------------------------------------------------
    # Close Connection
    # -----------------------------------------------------

    cursor.close()

    connection.close()


# =========================================================
# SILVER → MYSQL
# =========================================================

def load_silver(
    silver_file_path
):

    print(
        "Starting Silver to MySQL loading"
    )

    print(
        f"Reading Silver file from: "
        f"{silver_file_path}"
    )


    # -----------------------------------------------------
    # Read Silver File
    # -----------------------------------------------------

    df = pd.read_csv(
        silver_file_path
    )

    batch_id = df["batch_id"].iloc[0]
    print(
        f"Batch ID: "
        f"{batch_id}"
    )

    silver_count = len(
        df
    )

    print(
        f"Silver records found: "
        f"{silver_count}"
    )


    # -----------------------------------------------------
    # MySQL Connection
    # -----------------------------------------------------

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Insert Silver Data
    # -----------------------------------------------------

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
        final_price,
        batch_id
    )

    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )

    ON DUPLICATE KEY UPDATE

    customer_name = VALUES(customer_name),
    product = VALUES(product),
    price = VALUES(price),
    order_date = VALUES(order_date),
    price_category = VALUES(price_category),
    discount = VALUES(discount),
    final_price = VALUES(final_price),
    batch_id = VALUES(batch_id)

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
                row["batch_id"],
            )
        )


    cursor.executemany(
        query,
        data
    )

    connection.commit()


    print(
        f"Successfully loaded "
        f"{len(data)} Silver records "
        f"into MySQL"
    )


    # -----------------------------------------------------
    # Close Connection
    # -----------------------------------------------------

    cursor.close()

    connection.close()


# =========================================================
# GOLD → MYSQL
# =========================================================

def load_sales_summary(
    gold_file_path
):

    print(
        "Starting Gold to MySQL loading"
    )

    print(
        f"Reading Gold file from: "
        f"{gold_file_path}"
    )


    # -----------------------------------------------------
    # Read Gold File
    # -----------------------------------------------------

    df = pd.read_csv(
        gold_file_path
    )

    batch_id = df["batch_id"].iloc[0]

    print(
        f"Batch ID: "
        f"{batch_id}"
    )

    gold_count = len(
        df
    )

    print(
        f"Gold records found: "
        f"{gold_count}"
    )


    # -----------------------------------------------------
    # MySQL Connection
    # -----------------------------------------------------

    hook = MySqlHook(
        mysql_conn_id="retail_mysql"
    )

    connection = hook.get_conn()

    cursor = connection.cursor()


    # -----------------------------------------------------
    # Insert Gold Data
    # -----------------------------------------------------

    query = """

    INSERT INTO sales_summary
    (
        metric,
        value,
        batch_id
    )

    VALUES
    (
        %s,
        %s,
        %s
    )

    ON DUPLICATE KEY UPDATE

    value = VALUES(value),
    batch_id = VALUES(batch_id)

    """


    data = []

    for _, row in df.iterrows():

        data.append(
            (
                row["metric"],
                row["value"],
                row["batch_id"]
            )
        )


    cursor.executemany(
        query,
        data
    )

    connection.commit()


    print(
        f"Successfully loaded "
        f"{len(data)} Gold records "
        f"into MySQL"
    )


    # -----------------------------------------------------
    # Close Connection
    # -----------------------------------------------------

    cursor.close()

    connection.close()
