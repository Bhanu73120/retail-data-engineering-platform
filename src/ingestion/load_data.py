import pandas as pd
from src.utils.logger import logger

def load_csv(path):
    try:
        logger.info(f"Loading file: {path}")
        return pd.read_csv(path)

    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise  #If we remove it:The error is logged...but the program keeps going.