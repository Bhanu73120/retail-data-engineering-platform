import pandas as pd
from src.utils.logger import logger

def save_csv(df, path):
    try:
        logger.info(f"Saving file to: {path}")
        df.to_csv(path, index=False)
        logger.info("File saved successfully")

    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise