import pandas as pd
import numpy as np
from config.config import BRONZE_DATA_PATH,SILVER_DATA_PATH
from src.ingestion.load_data import load_csv
from src.warehouse.save_data import save_csv
from src.transformation.business_rules import apply_business_rules
from src.utils.logger import logger


def main():

    logger.info("Silver Layer Started")

    orders = load_csv(BRONZE_DATA_PATH)
    logger.info("Bronze data loaded successfully")

    orders = apply_business_rules(orders)
    logger.info("Business rules applied successfully")

    save_csv(orders, SILVER_DATA_PATH)
    logger.info("Silver data saved successfully")


if __name__ == "__main__":
    main()
