from src.utils.logger import logger

def validate_before_cleaning(df):
    validate_required_columns(df)
    validate_data_types(df)

def validate_after_cleaning(df):
    validate_missing_values(df)
    validate_price(df)
    validate_duplicate_orders(df)

def validate_required_columns(df):

    required_columns = [
        "order_id",
        "customer_name",
        "product",
        "price"
    ]

    for column in required_columns:

        if column not in df.columns:

            logger.error(f"Missing required column: {column}")

            raise ValueError(f"Missing required column: {column}")

    logger.info("All required columns are present.")


def validate_data_types(df):

    if not df["order_id"].dtype == "int64":
        logger.error("order_id should be integer")
        raise ValueError("order_id should be integer")

    if not df["price"].dtype in ["int64", "float64"]:
        logger.error("price should be numeric")
        raise ValueError("price should be numeric")

    logger.info("Data types validated successfully")


def validate_missing_values(df):

    required_columns = [
        "order_id",
        "customer_name",
        "product",
        "price"
    ]

    for column in required_columns:

        if df[column].isnull().any():

            logger.error(f"Missing values found in {column}")

            raise ValueError(f"Missing values found in {column}")

    logger.info("Mandatory fields validated")


def validate_price(df):

    if (df["price"] < 0).any():

        logger.error("Negative prices found")

        raise ValueError("Negative prices found")

    logger.info("Price validation successful")


def validate_duplicate_orders(df):

    if df["order_id"].duplicated().any():

        logger.error("Duplicate Order IDs found")

        raise ValueError("Duplicate Order IDs found")

    logger.info("Order ID validation successful")