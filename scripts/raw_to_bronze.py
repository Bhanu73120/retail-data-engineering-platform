import pandas as pd
from config.config import RAW_DATA_PATH, BRONZE_DATA_PATH
from src.ingestion.load_data import load_csv
from src.validation.validate_data import (
    validate_before_cleaning,
    validate_after_cleaning
)
from src.warehouse.save_data import save_csv
from src.transformation.customer import clean_customer_data
from src.transformation.duplicate import remove_duplicates
from src.transformation.product import clean_product_data
from src.utils.logger import logger

def main():
   logger.info("Bronze Layer Started")
   orders = load_csv(RAW_DATA_PATH)
   validate_before_cleaning(orders)

   logger.info("Raw data loaded successfully")
   
   orders = remove_duplicates(orders)
   logger.info("Duplicates removed")
   orders = clean_customer_data(orders)
   
   logger.info("Customer data cleaned")
   
   orders = clean_product_data(orders)
   validate_after_cleaning(orders)
   save_csv(orders,BRONZE_DATA_PATH)
   
   
   logger.info("Bronze data saved successfully")

if __name__ == "__main__":
    main()