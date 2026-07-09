import pandas as pd

from src.transformation.sales_summary import generate_sales_summary


def test_generate_sales_summary():

    data = pd.DataFrame({
        "order_id": [1, 2, 3],
        "final_price": [1000, 2000, 3000]
    })

    result = generate_sales_summary(data)

    assert result.loc[0, "value"] == 6000 #sum
    assert result.loc[1, "value"] == 3 #count
    assert result.loc[2, "value"] == 2000 #mean
    assert result.loc[3, "value"] == 3000 #max
    assert result.loc[4, "value"] == 1000 #min