from src.utils.logger import logger
import pandas as pd
from src.database import get_connection

connection = None #in finally we have this if there is exception our ide dont know about cursor so i wrote it as 0
cursor = None
success = False

try:
    logger.info("Starting Bronze to MySQL Loading Process")

    # Read Bronze Layer
    df = pd.read_csv("data/bronze/orders.csv")

    logger.info("Bronze data loaded successfully")

    # Connect to MySQL
    connection = get_connection()
    cursor = connection.cursor()

    logger.info("Connected to MySQL")

    # Insert records
    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO orders
            (order_id, customer_name, product, price, order_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                row["order_id"],
                row["customer_name"],
                row["product"],
                row["price"],
                row["order_date"]
            )
        )

    # Save transaction
    connection.commit()
    success = True

    logger.info("Data inserted successfully!")

except Exception as e:

    logger.error(f"Error while loading data: {e}")

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

    if success:
       logger.info("Bronze to MySQL ETL completed successfully")
    else:
       logger.error("Bronze to MySQL ETL failed")