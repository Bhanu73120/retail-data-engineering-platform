def clean_customer_data(orders):
    orders["customer_name"] = orders["customer_name"].fillna("Unknown")
    orders["customer_name"] = orders["customer_name"].str.strip()
    orders["customer_name"] = orders["customer_name"].str.title()
    return orders;