import pandas as pd
import numpy as np
from config.config import BRONZE_DATA_PATH,SILVER_DATA_PATH
from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv
from src.transformation.business_rules import apply_business_rules
from src.utils.logger import logger

# def load_data():
#     orders = pd.read_csv("data/bronze/orders.csv")
#     return orders;

# def save_data(orders):
#     orders.to_csv("data/silver/orders.csv",index =False)

logger.info("Silver layer Started")
orders = load_csv(BRONZE_DATA_PATH)
logger.info("Silver data loaded successfully")
orders = apply_business_rules(orders)
logger.info("Applied Business Rules")
save_csv(orders, SILVER_DATA_PATH)
logger.info("Silver Layer Stored Successfully")


#print("silver data stored succesfully")


# orders = pd.read_csv("data/bronze/orders.csv")

# orders["price_category"] = np.where(
#     orders["price"]>10000,
#     "high",
#     "low"
# )

# orders["discount"] = np.where(
#     orders["price"] >= 10000,
#     10,5
# )

# orders["final_price"] = orders["price"]-(
#     orders["price"]*orders["discount"]/100)

# print(orders)

#orders.to_csv("data/silver/orders.csv",index=False)

