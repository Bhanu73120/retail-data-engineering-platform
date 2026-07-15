import pandas as pd
import logging
import os
# Create folders
os.makedirs("data/raw", exist_ok=True)
os.makedirs("logs", exist_ok=True)
# Configure logging
logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ingest_orders():

    try:

        logging.info("Order ingestion started")

        # Source file
        source_path = "data/source/orders.csv"

        # Raw layer destination
        raw_path = "data/raw/orders_raw.csv"

        # Read source CSV

        orders = pd.read_csv(source_path)

        logging.info(
            f"Records extracted: {len(orders)}"
        )

        # Data validation

        if orders.empty:
            raise Exception(
                "Source file is empty"
            )

        # Save into Raw layer

        orders.to_csv(
            raw_path,
            index=False
        )


        logging.info(
            "Orders successfully loaded into Raw layer"
        )


        print(
            "Order ingestion completed successfully!"
        )


    except Exception as e:

        logging.error(
            f"Ingestion failed: {str(e)}"
        )

        print(
            "Order ingestion failed!"
        )


if __name__ == "__main__":

    ingest_orders()