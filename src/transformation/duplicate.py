def remove_duplicates(orders):
    orders = orders.drop_duplicates()
    return orders