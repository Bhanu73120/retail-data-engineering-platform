import pandas as pd
from config.config import SILVER_DATA_PATH,GOLD_DATA_PATH
from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv
from src.transformation.sales_summary import generate_sales_summary
from src.utils.logger import logger

def main():

    logger.info("Gold Layer Started")

    orders = load_csv(SILVER_DATA_PATH)
    logger.info("Silver data loaded successfully")

    summary = generate_sales_summary(orders)
    logger.info("Sales summary generated successfully")

    save_csv(summary, GOLD_DATA_PATH)
    logger.info("Gold data saved successfully")


if __name__ == "__main__":
    main()