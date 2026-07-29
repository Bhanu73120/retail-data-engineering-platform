import os

from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv

from src.transformation.sales_summary import (
    generate_sales_summary
)

from src.utils.logger import logger


# =========================================================
# SILVER → GOLD
# =========================================================

def transform_silver_to_gold(
    silver_file_path
):

    logger.info(
        "Gold Layer Started"
    )

    logger.info(
        f"Reading Silver file: {silver_file_path}"
    )


    # -----------------------------------------------------
    # Load Silver Data
    # -----------------------------------------------------

    orders = load_csv(
        silver_file_path
    )

    logger.info(
        f"Silver data loaded successfully. "
        f"Records: {len(orders)}"
    )


    # -----------------------------------------------------
    # Generate Sales Summary
    # -----------------------------------------------------

    summary = generate_sales_summary(
        orders
    )

    logger.info(
        "Sales summary generated successfully"
    )


    # -----------------------------------------------------
    # Generate Dynamic Gold File Path
    # -----------------------------------------------------

    silver_file_name = os.path.basename(
        silver_file_path
    )

    silver_file_name_without_extension = os.path.splitext(
        silver_file_name
    )[0]


    gold_file_name = (
        silver_file_name_without_extension
        .replace("_silver", "")
        + "_gold.csv"
    )


    gold_file_path = os.path.join(
        "data",
        "gold",
        gold_file_name
    )


    # -----------------------------------------------------
    # Save Data Into Gold Layer
    # -----------------------------------------------------

    save_csv(
        summary,
        gold_file_path
    )

    logger.info(
        f"Gold data saved successfully: "
        f"{gold_file_path}"
    )

    logger.info(
        f"Gold metrics generated: {len(summary)}"
    )


    # -----------------------------------------------------
    # Return Gold File Path
    #
    # Airflow TaskFlow API will pass this through XCom
    # -----------------------------------------------------

    return gold_file_path


# =========================================================
# LOCAL EXECUTION
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # This is ONLY for local testing.
    #
    # Airflow will provide the actual silver_file_path.
    # -----------------------------------------------------

    silver_file_path = (
        "data/silver/"
        "external_orders_messy_110_records_silver.csv"
    )


    transform_silver_to_gold(
        silver_file_path
    )