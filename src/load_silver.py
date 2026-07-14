import pandas as pd

from config.config import SILVER_DATA_PATH
from src.database import get_connection
from src.utils.logger import logger


def main():
    logger.info("Starting Silver to MySQL Loading Process")

    connection = None
    cursor = None

    try:
        df = pd.read_csv(SILVER_DATA_PATH)
        logger.info("Silver data loaded successfully")

        connection = get_connection()
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

        cursor.executemany(query, data)
        connection.commit()

        logger.info("Silver data inserted successfully!")

    except Exception as e:
        logger.error(f"Error while loading Silver data: {e}")

        if connection:
            connection.rollback()
            logger.warning("Transaction rolled back successfully")

    finally:
        if cursor:
            cursor.close()
            logger.info("Cursor closed")

        if connection:
            connection.close()
            logger.info("Database connection closed")

    logger.info("Silver to MySQL ETL completed successfully")


if __name__ == "__main__":
    main()