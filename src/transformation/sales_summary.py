import pandas as pd
def generate_sales_summary(orders):
    total_revenue = orders["final_price"].sum()
    total_orders = orders["order_id"].count()
    average_order = orders["final_price"].mean()
    highest_order = orders["final_price"].max()
    lowest_order = orders["final_price"].min()

    summary = pd.DataFrame({
        "metric": [
            "Total Revenue",
            "Total Orders",
            "Average Order Value",
            "Highest Order Value",
            "Lowest Order Value"
        ],
        "value": [
            total_revenue,
            total_orders,
            average_order,
            highest_order,
            lowest_order
        ]
    })

    return summary