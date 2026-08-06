import pandas as pd


def generate_sales_summary(orders):

    total_revenue = orders["final_price"].sum()
    total_orders = orders["order_id"].count()
    average_order = orders["final_price"].mean()
    highest_order = orders["final_price"].max()
    lowest_order = orders["final_price"].min()

    batch_id = orders["batch_id"].iloc[0]
    source_file = orders["source_file"].iloc[0]
    ingestion_timestamp = orders["ingestion_timestamp"].iloc[0]

    metrics = [
        "Total Revenue",
        "Total Orders",
        "Average Order Value",
        "Highest Order Value",
        "Lowest Order Value"
    ]

    values = [
        total_revenue,
        total_orders,
        average_order,
        highest_order,
        lowest_order
    ]

    summary = pd.DataFrame({
        "metric": metrics,
        "value": values,
        "batch_id": [batch_id] * len(metrics),
        "source_file": [source_file] * len(metrics),
        "ingestion_timestamp": [ingestion_timestamp] * len(metrics)
    })

    return summary