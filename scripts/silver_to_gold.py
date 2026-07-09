import pandas as pd
from config.config import SILVER_DATA_PATH,GOLD_DATA_PATH
from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv
from src.transformation.sales_summary import generate_sales_summary
from src.utils.logger import logger

# def load_data():
#     return pd.read_csv("data/silver/orders.csv")



# def save_data(summary):
#     print(type(summary))
#     summary.to_csv("data/gold/sales_summary.csv", index=False)

logger.info("GOld Layer Started")
orders = load_csv(SILVER_DATA_PATH)
logger.info("Gold data loaded successfully")
summary = generate_sales_summary(orders)
logger.info("Sales Summary Generated")
save_csv(summary, GOLD_DATA_PATH)
logger.info("Gold Layer Stored Successfully")

#print("gold data stored succesfully")