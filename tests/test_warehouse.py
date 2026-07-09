import pandas as pd
import pytest

from src.warehouse.save_data import save_csv


def test_save_csv(tmp_path):

    data = pd.DataFrame({
        "id": [1, 2],
        "name": ["Bhanu", "Rahul"]
    })

    file_path = tmp_path / "output.csv"

    save_csv(data, file_path)

    assert file_path.exists()

    saved = pd.read_csv(file_path)

    assert len(saved) == 2


def test_save_csv_failure(tmp_path):

    data = pd.DataFrame({
        "id": [1]
    })

    invalid_path = tmp_path / "abc" / "output.csv"

    with pytest.raises(OSError):
        save_csv(data, invalid_path)