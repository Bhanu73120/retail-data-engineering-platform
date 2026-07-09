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



# def load_data():
#     orders = pd.read_csv("data/raw/orders.csv")
#     return orders

# def save_data(orders):
#     orders.to_csv("data/bronze/orders.csv", index=False)

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


#print("Bronze created succesfully")



# orders = pd.read_csv("data/raw/orders.csv")
# print("Raw Data:")
# print(orders)

# orders = orders.drop_duplicates()
# print("\nAfter Removing Duplicates:")
# print(orders)

# print("\nMissing Values:")
# print(orders.isnull())

# print("\nMissing Values Count:")
# print(orders.isnull().sum())

# orders["customer_name"] = orders["customer_name"].fillna("Unknown")
# orders["product"] = orders["product"].fillna("Unknown")

# print("\nAfter Handling Missing Values:")
# print(orders)

# orders["customer_name"] = orders["customer_name"].str.title()
# orders["customer_name"] = orders["customer_name"].str.strip()
# print("\nAfter Standardizing Customer Names:")
# print(orders)

# orders.to_csv("data/bronze/orders.csv", index=False)

# print("\nBronze layer created successfully!")