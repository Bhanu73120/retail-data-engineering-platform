import os
import pandas as pd

from src.ingestion.load_data import load_csv

from src.validation.validate_data import (
    validate_before_cleaning,
    validate_after_cleaning
)

from src.warehouse.save_data import save_csv

from src.transformation.customer import (
    clean_customer_data
)

from src.transformation.duplicate import (
    remove_duplicates
)

from src.transformation.product import (
    clean_product_data
)

from src.utils.logger import logger


# =========================================================
# RAW → BRONZE
# =========================================================

def transform_raw_to_bronze(raw_file_path):

    logger.info(
        "Bronze Layer Started"
    )

    logger.info(
        f"Reading Raw file: {raw_file_path}"
    )


    # -----------------------------------------------------
    # Load Raw CSV
    # -----------------------------------------------------

    orders = load_csv(
        raw_file_path
    )


    # -----------------------------------------------------
    # Validate Before Cleaning
    # -----------------------------------------------------

    validate_before_cleaning(
        orders
    )


    logger.info(
        f"Raw data loaded successfully. "
        f"Records: {len(orders)}"
    )


    # -----------------------------------------------------
    # Remove Duplicates
    # -----------------------------------------------------

    orders = remove_duplicates(
        orders
    )

    logger.info(
        f"Duplicates removed. "
        f"Records remaining: {len(orders)}"
    )


    # -----------------------------------------------------
    # Clean Customer Data
    # -----------------------------------------------------

    orders = clean_customer_data(
        orders
    )

    logger.info(
        "Customer data cleaned"
    )


    # -----------------------------------------------------
    # Clean Product Data
    # -----------------------------------------------------

    orders = clean_product_data(
        orders
    )

    logger.info(
        "Product data cleaned"
    )


    # -----------------------------------------------------
    # Validate After Cleaning
    # -----------------------------------------------------

    validate_after_cleaning(
        orders
    )


    # -----------------------------------------------------
    # Generate Dynamic Bronze File Path
    # -----------------------------------------------------

    raw_file_name = os.path.basename(
        raw_file_path
    )

    raw_file_name_without_extension = os.path.splitext(
        raw_file_name
    )[0]


    # Remove "_raw" from the filename

    bronze_file_name = (
        raw_file_name_without_extension
        .replace("_raw", "")
        + "_bronze.csv"
    )


    bronze_file_path = os.path.join(
        "data",
        "bronze",
        bronze_file_name
    )


    # -----------------------------------------------------
    # Save Cleaned Data Into Bronze Layer
    # -----------------------------------------------------

    save_csv(
        orders,
        bronze_file_path
    )


    logger.info(
        f"Bronze data saved successfully: "
        f"{bronze_file_path}"
    )


    logger.info(
        f"Bronze records: {len(orders)}"
    )


    # -----------------------------------------------------
    # Return Bronze File Path
    #
    # Airflow TaskFlow API will pass this through XCom
    # -----------------------------------------------------

    return bronze_file_path


# =========================================================
# LOCAL EXECUTION
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # This is ONLY for local testing.
    #
    # Airflow will provide the actual raw_file_path.
    # -----------------------------------------------------

    raw_file_path = (
        "data/raw/external_orders_messy_110_records_raw.csv"
    )


    transform_raw_to_bronze(
        raw_file_path
    )