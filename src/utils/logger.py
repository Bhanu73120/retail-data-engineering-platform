import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",

    handlers=[
        logging.FileHandler("logs/etl.log"), #Save every log to:logs/etl.log
        logging.StreamHandler() #show logs in the terminal too.
    ]
)

logger = logging.getLogger(__name__)