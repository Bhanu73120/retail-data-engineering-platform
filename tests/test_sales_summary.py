import pandas as pd

from src.transformation.sales_summary import generate_sales_summary


def test_generate_sales_summary():

    data = pd.DataFrame({
        "order_id": [1, 2, 3],
        "final_price": [1000, 2000, 3000],
        "batch_id": ["BATCH_TEST"] * 3,
        "source_file": ["test_orders.csv"] * 3,
        "ingestion_timestamp": ["2026-10-07 10:00:00"] * 3
    })

    result = generate_sales_summary(data)

    # Test calculated metrics
    assert result.loc[0, "value"] == 6000
    assert result.loc[1, "value"] == 3
    assert result.loc[2, "value"] == 2000
    assert result.loc[3, "value"] == 3000
    assert result.loc[4, "value"] == 1000

    # Test batch metadata
    assert result.loc[0, "batch_id"] == "BATCH_TEST"
    assert result.loc[0, "source_file"] == "test_orders.csv"
    assert result.loc[0, "ingestion_timestamp"] == "2026-10-07 10:00:00"