def clean_product_data(orders):
    orders["product"] = orders["product"].fillna("Unknown")
    orders["product"] = orders["product"].str.strip()
    orders["product"] = orders["product"].str.title()
    return orders;