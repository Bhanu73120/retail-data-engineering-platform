import numpy as np


def apply_business_rules(orders):

    # Price Category
    orders["price_category"] = np.select(
        [
            orders["price"] >= 50000,
            orders["price"] >= 10000
        ],
        [
            "High",
            "Medium"
        ],
        default="Low"
    )

    # Discount Percentage
    orders["discount"] = np.select(
        [
            orders["price_category"] == "High",
            orders["price_category"] == "Medium"
        ],
        [
            15,
            10
        ],
        default=5
    )

    # Final Price
    orders["final_price"] = (
        orders["price"]
        - (orders["price"] * orders["discount"] / 100)
    )

    return orders