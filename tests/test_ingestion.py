import pandas as pd
import pytest

from src.ingestion.load_data import load_csv

import pandas as pd

from src.ingestion.load_data import load_csv

def test_load_csv_success(tmp_path):

    data = pd.DataFrame({
        "id": [1, 2],
        "name": ["Bhanu", "Rahul"]
    })

    file_path = tmp_path / "orders.csv"

    data.to_csv(file_path, index=False)

    result = load_csv(file_path)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2



# def test_load_csv_success():

#     result = load_csv("data/raw/orders.csv")
    #here we use data/raw/orders.csv waht if after some days so pytest give option called
    #tmp_path by which we can create a dummy csv so that is why i commented all this code

    # assert isinstance(result, pd.DataFrame)


# def test_load_csv_file_not_found():

#     with pytest.raises(FileNotFoundError):
#         load_csv("data/raw/abc.csv")