import pandas as pd

from config.config import GOLD_DATA_PATH
from src.database import get_connection
from src.utils.logger import logger


def main():
    logger.info("Starting Gold to MySQL Loading Process")

    connection = None
    cursor = None

    try:
        # Load Gold CSV
        df = pd.read_csv(GOLD_DATA_PATH)
        logger.info("Gold data loaded successfully")

        # Connect to MySQL
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO sales_summary
        (
            metric,
            value
        )
        VALUES (%s, %s)

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

        cursor.executemany(query, data)

        connection.commit()

        logger.info("Gold data inserted successfully!")

    except Exception as e:
        logger.error(f"Error while loading Gold data: {e}")

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

    logger.info("Gold to MySQL ETL completed successfully")


if __name__ == "__main__":
    main()