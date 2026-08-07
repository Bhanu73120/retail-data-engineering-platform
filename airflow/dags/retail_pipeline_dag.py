import sys
import os
import glob
import shutil
import uuid

from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.exceptions import AirflowSkipException


# =========================================================
# PROJECT CONFIGURATION
# =========================================================

PROJECT_PATH = Variable.get(
    "PROJECT_PATH"
)

EXTERNAL_FOLDER_PATH = Variable.get(
    "EXTERNAL_FOLDER_PATH"
)


# ---------------------------------------------------------
# Add project path so Airflow can import project modules
# ---------------------------------------------------------

sys.path.insert(
    0,
    PROJECT_PATH
)


# =========================================================
# IMPORT MYSQL LOADING FUNCTIONS
# =========================================================

from src.warehouse.mysql_loader import (
    load_orders,
    load_silver,
    load_sales_summary
)


# =========================================================
# DEFAULT DAG ARGUMENTS
# =========================================================

default_args = {
    "owner": "bhanu",
    "depends_on_past": False,
    "retries": 0,
}


# =========================================================
# 1. INGEST EXTERNAL CSV
# =========================================================

@task
def ingest_orders():

    print(
        "Starting external CSV ingestion"
    )


    # -----------------------------------------------------
    # Incoming folder
    # -----------------------------------------------------

    incoming_folder = os.path.join(
        EXTERNAL_FOLDER_PATH,
        "incoming"
    )


    print(
        f"Searching for new CSV files in: "
        f"{incoming_folder}"
    )


    # -----------------------------------------------------
    # Create processed folder
    # -----------------------------------------------------

    processed_folder = os.path.join(
        EXTERNAL_FOLDER_PATH,
        "processed"
    )


    os.makedirs(
        processed_folder,
        exist_ok=True
    )


    # -----------------------------------------------------
    # Find CSV files directly inside incoming folder
    # -----------------------------------------------------

    external_files = glob.glob(
        os.path.join(
            incoming_folder,
            "*.csv"
        )
    )


    # -----------------------------------------------------
    # Check if CSV exists
    # -----------------------------------------------------

    if not external_files:
       print("No new CSV files found in incoming folder.")
       raise AirflowSkipException(
           "Skipping DAG. No files available."
        )

    # -----------------------------------------------------
    # Select oldest CSV
    #
    # If multiple CSV files exist,
    # only ONE file is processed per DAG run.
    # -----------------------------------------------------

    source_path = min(
        external_files,
        key=os.path.getmtime
    )


    print(
        f"New external CSV found: "
        f"{source_path}"
    )


    # -----------------------------------------------------
    # Generate dynamic Raw file path
    # -----------------------------------------------------

    file_name = os.path.basename(
        source_path
    )


    file_name_without_extension = os.path.splitext(
        file_name
    )[0]


    raw_file_path = os.path.join(
        PROJECT_PATH,
        "data",
        "raw",
        f"{file_name_without_extension}_raw.csv"
    )


    # -----------------------------------------------------
    # Read External CSV
    # -----------------------------------------------------

    import pandas as pd


    orders = pd.read_csv(
        source_path
    )

    # -----------------------------------------------------
# Generate Batch ID
# -----------------------------------------------------

    batch_id = (
    f"BATCH_{uuid.uuid4().hex[:8].upper()}"
    )

    print(
    f"Generated Batch ID: "
    f"{batch_id}"
    )

    orders["batch_id"] = batch_id

    # -----------------------------------------------------
    # Pipeline Metadata
    # -----------------------------------------------------

    source_file = file_name

    ingestion_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    orders["source_file"] = source_file

    orders["ingestion_timestamp"] = ingestion_timestamp


    raw_count = len(
        orders
    )


    print(
        f"Records extracted from external CSV: "
        f"{raw_count}"
    )


    # -----------------------------------------------------
    # Validate Source Data
    # -----------------------------------------------------

    if orders.empty:

        raise ValueError(
            "External CSV file is empty"
        )


    # -----------------------------------------------------
    # Save Into Raw Layer
    # -----------------------------------------------------

    orders.to_csv(
        raw_file_path,
        index=False
    )


    print(
        f"Raw file created: "
        f"{raw_file_path}"
    )


    print(
        f"Raw records: "
        f"{raw_count}"
    )



    # -----------------------------------------------------
    # Move successfully ingested CSV
    # to processed folder
    # -----------------------------------------------------

    processed_file_path = os.path.join(
        processed_folder,
        file_name
    )


    shutil.move(
        source_path,
        processed_file_path
    )


    print(
        f"External CSV moved to processed folder: "
        f"{processed_file_path}"
    )


    # -----------------------------------------------------
    # Return ingestion result through XCom
    # -----------------------------------------------------

    return {
        "batch_id": batch_id,
        "source_file": source_file,
        "ingestion_timestamp": ingestion_timestamp,
        "raw_file_path": raw_file_path,
        "raw_count": raw_count
    }


# =========================================================
# 2. RAW → BRONZE
# =========================================================

@task
def transform_raw_to_bronze(
    ingestion_result
):

    import os

    from src.ingestion.load_data import (
        load_csv
    )

    from src.validation.validate_data import (
        validate_before_cleaning,
        validate_after_cleaning
    )

    from src.warehouse.save_data import (
        save_csv
    )

    from src.transformation.customer import (
        clean_customer_data
    )

    from src.transformation.duplicate import (
        remove_duplicates
    )

    from src.transformation.product import (
        clean_product_data
    )


    # -----------------------------------------------------
    # Get Raw File Path
    # -----------------------------------------------------

    raw_file_path = ingestion_result[
        "raw_file_path"
    ]


    print(
        f"Reading Raw file: "
        f"{raw_file_path}"
    )


    # -----------------------------------------------------
    # Load Raw Data
    # -----------------------------------------------------

    orders = load_csv(
        raw_file_path
    )


    print(
        f"Raw records found: "
        f"{len(orders)}"
    )


    # -----------------------------------------------------
    # Validate Before Cleaning
    # -----------------------------------------------------

    validate_before_cleaning(
        orders
    )


    # -----------------------------------------------------
    # Remove Duplicates
    # -----------------------------------------------------

    orders = remove_duplicates(
        orders
    )


    print(
        f"Records after duplicate removal: "
        f"{len(orders)}"
    )


    # -----------------------------------------------------
    # Clean Customer Data
    # -----------------------------------------------------

    orders = clean_customer_data(
        orders
    )


    print(
        "Customer data cleaned"
    )


    # -----------------------------------------------------
    # Clean Product Data
    # -----------------------------------------------------

    orders = clean_product_data(
        orders
    )


    print(
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


    bronze_file_path = os.path.join(
        PROJECT_PATH,
        "data",
        "bronze",
        f"{raw_file_name_without_extension.replace('_raw', '')}_bronze.csv"
    )


    # -----------------------------------------------------
    # Save Bronze Data
    # -----------------------------------------------------

    save_csv(
        orders,
        bronze_file_path
    )


    print(
        f"Bronze file created: "
        f"{bronze_file_path}"
    )


    print(
        f"Bronze records: "
        f"{len(orders)}"
    )

    print(
        f"Batch ID: "
        f"{ingestion_result['batch_id']}"
    )


    # -----------------------------------------------------
    # Return Bronze Path + Count
    # -----------------------------------------------------

    return {
        "bronze_file_path": bronze_file_path,
        "bronze_count": len(orders)
    }


# =========================================================
# 3. LOAD BRONZE INTO MYSQL
# =========================================================

@task
def load_bronze(
    bronze_result
):

    bronze_file_path = bronze_result[
        "bronze_file_path"
    ]


    bronze_count = bronze_result[
        "bronze_count"
    ]
    

    print(
        f"Loading Bronze file into MySQL: "
        f"{bronze_file_path}"
    )


    load_orders(
        bronze_file_path
    )


    print(
        f"Bronze records loaded into MySQL: "
        f"{bronze_count}"
    )



    return bronze_count


# =========================================================
# 4. BRONZE → SILVER
# =========================================================

@task
def transform_bronze_to_silver(
    bronze_result
):

    import os

    from src.ingestion.load_data import (
        load_csv
    )

    from src.warehouse.save_data import (
        save_csv
    )

    from src.transformation.business_rules import (
        apply_business_rules
    )


    # -----------------------------------------------------
    # Get Bronze File Path
    # -----------------------------------------------------

    bronze_file_path = bronze_result[
        "bronze_file_path"
    ]


    print(
        f"Reading Bronze file: "
        f"{bronze_file_path}"
    )


    # -----------------------------------------------------
    # Load Bronze Data
    # -----------------------------------------------------

    orders = load_csv(
        bronze_file_path
    )


    print(
        f"Bronze records found: "
        f"{len(orders)}"
    )


    # -----------------------------------------------------
    # Apply Business Rules
    # -----------------------------------------------------

    orders = apply_business_rules(
        orders
    )


    print(
        "Business rules applied successfully"
    )


    # -----------------------------------------------------
    # Generate Dynamic Silver Path
    # -----------------------------------------------------

    bronze_file_name = os.path.basename(
        bronze_file_path
    )


    bronze_file_name_without_extension = os.path.splitext(
        bronze_file_name
    )[0]


    silver_file_path = os.path.join(
        PROJECT_PATH,
        "data",
        "silver",
        f"{bronze_file_name_without_extension.replace('_bronze', '')}_silver.csv"
    )


    # -----------------------------------------------------
    # Save Silver Data
    # -----------------------------------------------------

    save_csv(
        orders,
        silver_file_path
    )


    print(
        f"Silver file created: "
        f"{silver_file_path}"
    )


    print(
        f"Silver records: "
        f"{len(orders)}"
    )

    batch_id = orders["batch_id"].iloc[0]
    print(
        f"Batch ID: "
        f"{batch_id}"
    )


    # -----------------------------------------------------
    # Return Silver Path + Count
    # -----------------------------------------------------

    return {
        "silver_file_path": silver_file_path,
        "silver_count": len(orders)
    }


# =========================================================
# 5. LOAD SILVER INTO MYSQL
# =========================================================

@task
def load_silver_data(
    silver_result
):

    silver_file_path = silver_result[
        "silver_file_path"
    ]


    silver_count = silver_result[
        "silver_count"
    ]



    print(
        f"Loading Silver file into MySQL: "
        f"{silver_file_path}"
    )


    load_silver(
        silver_file_path
    )


    print(
        f"Silver records loaded into MySQL: "
        f"{silver_count}"
    )



    return silver_count


# =========================================================
# 6. SILVER → GOLD
# =========================================================

@task
def transform_silver_to_gold(
    silver_result
):

    import os

    from src.ingestion.load_data import (
        load_csv
    )

    from src.warehouse.save_data import (
        save_csv
    )

    from src.transformation.sales_summary import (
        generate_sales_summary
    )


    # -----------------------------------------------------
    # Get Silver File Path
    # -----------------------------------------------------

    silver_file_path = silver_result[
        "silver_file_path"
    ]


    print(
        f"Reading Silver file: "
        f"{silver_file_path}"
    )


    # -----------------------------------------------------
    # Load Silver Data
    # -----------------------------------------------------

    orders = load_csv(
        silver_file_path
    )
    batch_id = orders["batch_id"].iloc[0]


    print(
        f"Silver records found: "
        f"{len(orders)}"
    )


    # -----------------------------------------------------
    # Generate Sales Summary
    # -----------------------------------------------------

    summary = generate_sales_summary(
        orders
    )


    print(
        "Sales summary generated successfully"
    )


    # -----------------------------------------------------
    # Generate Dynamic Gold Path
    # -----------------------------------------------------

    silver_file_name = os.path.basename(
        silver_file_path
    )


    silver_file_name_without_extension = os.path.splitext(
        silver_file_name
    )[0]


    gold_file_path = os.path.join(
        PROJECT_PATH,
        "data",
        "gold",
        f"{silver_file_name_without_extension.replace('_silver', '')}_gold.csv"
    )


    # -----------------------------------------------------
    # Save Gold Data
    # -----------------------------------------------------

    save_csv(
        summary,
        gold_file_path
    )


    print(
        f"Gold file created: "
        f"{gold_file_path}"
    )


    print(
        f"Gold metrics: "
        f"{len(summary)}"
    )

    print(
        f"Batch ID: "
        f"{batch_id}"
    )


    # -----------------------------------------------------
    # Return Gold Path + Count
    # -----------------------------------------------------

    return {
        "gold_file_path": gold_file_path,
        "gold_count": len(summary)
    }


# =========================================================
# 7. LOAD GOLD INTO MYSQL
# =========================================================

@task
def load_gold(
    gold_result
):

    gold_file_path = gold_result[
        "gold_file_path"
    ]


    gold_count = gold_result[
        "gold_count"
    ]


    print(
        f"Loading Gold file into MySQL: "
        f"{gold_file_path}"
    )


    load_sales_summary(
        gold_file_path
    )


    print(
        f"Gold metrics loaded into MySQL: "
        f"{gold_count}"
    )



    return gold_count


# =========================================================
# 8. DISPLAY PIPELINE SUMMARY
# =========================================================

@task
def display_pipeline_summary(
    ingestion_result,
    bronze_count,
    silver_count,
    gold_count
):

    batch_id = ingestion_result["batch_id"]
    source_file = ingestion_result["source_file"]
    ingestion_timestamp = ingestion_result["ingestion_timestamp"]

    raw_count = ingestion_result[
        "raw_count"
    ]


    print("")

    print(
        "=========================================="
    )

    print(
        "       RETAIL PIPELINE DATA SUMMARY"
    )

    print(
        "=========================================="
    )
 
    print(
        f"Batch ID         : {batch_id}"
    )

    print(
        f"Source File      : {source_file}"
    )

    print(
        f"Ingestion Time   : {ingestion_timestamp}"
    )

    print(
        f"Raw Records      : {raw_count}"
    )

    print(
        f"Bronze Records   : {bronze_count}"
    )

    print(
        f"Silver Records   : {silver_count}"
    )

    print(
        f"Gold Metrics     : {gold_count}"
    )


    print(
        "=========================================="
    )


    # -----------------------------------------------------
    # Raw → Bronze Difference
    # -----------------------------------------------------

    if raw_count != bronze_count:

        print(
            f"Raw → Bronze Difference : "
            f"{raw_count - bronze_count} records"
        )


    # -----------------------------------------------------
    # Bronze → Silver Difference
    # -----------------------------------------------------

    if bronze_count != silver_count:

        print(
            f"Bronze → Silver Difference : "
            f"{bronze_count - silver_count} records"
        )


    print(
        "=========================================="
    )


# =========================================================
# DAG DEFINITION
# =========================================================

with DAG(

    dag_id="retail_data_pipeline",

    default_args=default_args,

    description=(
        "Dynamic Retail Data Engineering ETL Pipeline"
    ),

    start_date=datetime(
        2026,
        7,
        1
    ),

    schedule="@daily",

    catchup=False,

    tags=[
        "retail",
        "etl",
        "mysql",
        "dynamic"
    ],

) as dag:


    # =====================================================
    # 1. INGEST EXTERNAL CSV
    # =====================================================

    ingestion_result = ingest_orders()


    # =====================================================
    # 2. RAW → BRONZE
    # =====================================================

    bronze_result = transform_raw_to_bronze(
        ingestion_result
    )


    # =====================================================
    # 3. LOAD BRONZE INTO MYSQL
    # =====================================================

    bronze_count = load_bronze(
        bronze_result
    )


    # =====================================================
    # 4. BRONZE → SILVER
    # =====================================================

    silver_result = transform_bronze_to_silver(
        bronze_result
    )


    # =====================================================
    # 5. LOAD SILVER INTO MYSQL
    # =====================================================

    silver_count = load_silver_data(
        silver_result
    )


    # =====================================================
    # 6. SILVER → GOLD
    # =====================================================

    gold_result = transform_silver_to_gold(
        silver_result
    )


    # =====================================================
    # 7. LOAD GOLD INTO MYSQL
    # =====================================================

    gold_count = load_gold(
        gold_result
    )


    # =====================================================
    # 8. PIPELINE SUMMARY
    # =====================================================

    pipeline_summary = display_pipeline_summary(

        ingestion_result,

        bronze_count,

        silver_count,

        gold_count

    )


    # =====================================================
    # TASK DEPENDENCIES
    # =====================================================

    ingestion_result >> bronze_result

    bronze_result >> bronze_count

    bronze_result >> silver_result

    silver_result >> silver_count

    silver_result >> gold_result

    gold_result >> gold_count


    [
        ingestion_result,
        bronze_count,
        silver_count,
        gold_count,

    ] >> pipeline_summary