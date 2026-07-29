import pandas as pd
import logging
import os
import glob
import shutil

# ---------------------------------------------------------
# Create Required Folders
# ---------------------------------------------------------

os.makedirs("data/external", exist_ok=True)
os.makedirs("data/external/processed", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------------
# Ingest External CSV
# ---------------------------------------------------------

def ingest_orders():

    try:

        logging.info(
            "External order ingestion started"
        )


        # -------------------------------------------------
        # Find CSV files waiting in external folder
        # -------------------------------------------------

        external_files = glob.glob(
            "data/external/*.csv"
        )


        # -------------------------------------------------
        # Check if a new CSV exists
        # -------------------------------------------------

        if not external_files:

            raise Exception(
                "No new CSV files found in data/external"
            )


        # -------------------------------------------------
        # Pick the first available CSV
        # -------------------------------------------------

        source_path = external_files[0]

        logging.info(
            f"External CSV found: {source_path}"
        )


        # -------------------------------------------------
        # Generate Raw File Name
        # -------------------------------------------------

        file_name = os.path.basename(
            source_path
        )

        file_name_without_extension = os.path.splitext(
            file_name
        )[0]


        raw_path = os.path.join(
            "data",
            "raw",
            f"{file_name_without_extension}_raw.csv"
        )


        # -------------------------------------------------
        # Read External CSV
        # -------------------------------------------------

        orders = pd.read_csv(
            source_path
        )


        logging.info(
            f"Records extracted: {len(orders)}"
        )


        # -------------------------------------------------
        # Data Validation
        # -------------------------------------------------

        if orders.empty:

            raise Exception(
                "Source CSV is empty"
            )


        # -------------------------------------------------
        # Save Into Raw Layer
        # -------------------------------------------------

        orders.to_csv(
            raw_path,
            index=False
        )


        logging.info(
            f"Orders successfully loaded into Raw layer: "
            f"{raw_path}"
        )


        # -------------------------------------------------
        # Move Processed CSV
        # -------------------------------------------------

        processed_path = os.path.join(
            "data",
            "external",
            "processed",
            file_name
        )


        shutil.move(
            source_path,
            processed_path
        )


        logging.info(
            f"External CSV moved to processed folder: "
            f"{processed_path}"
        )


        # -------------------------------------------------
        # Print Ingestion Summary
        # -------------------------------------------------

        print(
            "=========================================="
        )

        print(
            "External order ingestion completed!"
        )

        print(
            f"Source file    : {source_path}"
        )

        print(
            f"Raw file       : {raw_path}"
        )

        print(
            f"Processed file : {processed_path}"
        )

        print(
            f"Records ingested: {len(orders)}"
        )

        print(
            "=========================================="
        )


        # -------------------------------------------------
        # Return Raw File Path
        #
        # Airflow TaskFlow API can pass this value
        # to the next task through XCom.
        # -------------------------------------------------

        return raw_path


    except Exception as e:

        logging.error(
            f"Ingestion failed: {str(e)}"
        )


        print(
            f"Order ingestion failed: {str(e)}"
        )


        raise


# ---------------------------------------------------------
# Run Locally
# ---------------------------------------------------------

if __name__ == "__main__":

    ingest_orders()