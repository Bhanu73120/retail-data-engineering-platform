import pandas as pd

from src.transformation.duplicate import remove_duplicates
from src.transformation.customer import clean_customer_data
from src.transformation.product import clean_product_data
from src.transformation.business_rules import apply_business_rules


def test_remove_duplicates():

    data = pd.DataFrame({
        "order_id": [1, 1, 2]
    })

    result = remove_duplicates(data)

    assert len(result) == 2


def test_clean_customer_data():

    data = pd.DataFrame({
        "customer_name": [None, "  bhanu ", "RAHUL"]
    })

    result = clean_customer_data(data)

    assert result.loc[0, "customer_name"] == "Unknown"
    assert result.loc[1, "customer_name"] == "Bhanu"
    assert result.loc[2, "customer_name"] == "Rahul"


def test_clean_product_data():

    data = pd.DataFrame({
        "product": [None, "  laptop ", "mobile"]
    })

    result = clean_product_data(data)

    assert result.loc[0, "product"] == "Unknown"
    assert result.loc[1, "product"] == "Laptop"
    assert result.loc[2, "product"] == "Mobile"


def test_apply_business_rules():

    data = pd.DataFrame({
        "price": [5000, 15000]
    })

    result = apply_business_rules(data)

    assert result.loc[0, "price_category"] == "low"
    assert result.loc[1, "price_category"] == "high"

    assert result.loc[0, "discount"] == 5
    assert result.loc[1, "discount"] == 10

    assert result.loc[0, "final_price"] == 4750
    assert result.loc[1, "final_price"] == 13500