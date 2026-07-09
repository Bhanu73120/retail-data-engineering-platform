import numpy as np
def apply_business_rules(orders):
    orders["price_category"] = np.where(
        orders["price"]>10000,
        "high",
        "low"
    )
    
    orders["discount"] = np.where(
        orders["price"]>10000,
        10,
        5
    )

    orders["final_price"] = orders["price"]-(orders["price"]*orders["discount"]/100)

    return orders