import os
import pandas as pd

from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv

from src.transformation.business_rules import (
    apply_business_rules
)

from src.utils.logger import logger


# =========================================================
# BRONZE → SILVER
# =========================================================

def transform_bronze_to_silver(
    bronze_file_path
):

    logger.info(
        "Silver Layer Started"
    )

    logger.info(
        f"Reading Bronze file: {bronze_file_path}"
    )


    # -----------------------------------------------------
    # Load Bronze Data
    # -----------------------------------------------------

    orders = load_csv(
        bronze_file_path
    )

    logger.info(
        f"Bronze data loaded successfully. "
        f"Records: {len(orders)}"
    )


    # -----------------------------------------------------
    # Apply Business Rules
    # -----------------------------------------------------

    orders = apply_business_rules(
        orders
    )

    logger.info(
        "Business rules applied successfully"
    )


    # -----------------------------------------------------
    # Generate Dynamic Silver File Path
    # -----------------------------------------------------

    bronze_file_name = os.path.basename(
        bronze_file_path
    )

    bronze_file_name_without_extension = os.path.splitext(
        bronze_file_name
    )[0]


    silver_file_name = (
        bronze_file_name_without_extension
        .replace("_bronze", "")
        + "_silver.csv"
    )


    silver_file_path = os.path.join(
        "data",
        "silver",
        silver_file_name
    )


    # -----------------------------------------------------
    # Save Data Into Silver Layer
    # -----------------------------------------------------

    save_csv(
        orders,
        silver_file_path
    )

    logger.info(
        f"Silver data saved successfully: "
        f"{silver_file_path}"
    )

    logger.info(
        f"Silver records: {len(orders)}"
    )


    # -----------------------------------------------------
    # Return Silver File Path
    #
    # Airflow TaskFlow API will pass this through XCom
    # -----------------------------------------------------

    return silver_file_path


# =========================================================
# LOCAL EXECUTION
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # This is ONLY for local testing.
    #
    # Airflow will provide the actual bronze_file_path.
    # -----------------------------------------------------

    bronze_file_path = (
        "data/bronze/"
        "external_orders_messy_110_records_bronze.csv"
    )


    transform_bronze_to_silver(
        bronze_file_path
    )