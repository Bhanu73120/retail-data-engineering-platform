import pytest
import pandas as pd

from src.validation.validate_data import (
    validate_required_columns,
    validate_data_types,
    validate_missing_values,
    validate_price,
    validate_duplicate_orders,
    validate_before_cleaning,
    validate_after_cleaning,
)

def test_validate_before_cleaning():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    validate_before_cleaning(data)


def test_validate_after_cleaning():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    validate_after_cleaning(data)


def test_validate_required_columns_success():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    validate_required_columns(data)


def test_validate_required_columns_failure():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"]
    })

    with pytest.raises(ValueError):
        validate_required_columns(data)


def test_validate_data_types_success():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    validate_data_types(data)


def test_validate_data_types_failure():

    data = pd.DataFrame({
        "order_id": ["ABC"],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    with pytest.raises(ValueError):
        validate_data_types(data)


def test_validate_missing_values_success():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": ["Bhanu"],
        "product": ["Laptop"],
        "price": [1000]
    })

    validate_missing_values(data)


def test_validate_missing_values_failure():

    data = pd.DataFrame({
        "order_id": [1],
        "customer_name": [None],
        "product": ["Laptop"],
        "price": [1000]
    })

    with pytest.raises(ValueError):
        validate_missing_values(data)


def test_validate_price_valid():

    data = pd.DataFrame({
        "price": [100, 200, 300]
    })

    validate_price(data)


def test_validate_price_invalid():

    data = pd.DataFrame({
        "price": [100, -50, 300]
    })

    with pytest.raises(ValueError):
        validate_price(data)


def test_validate_duplicate_orders_success():

    data = pd.DataFrame({
        "order_id": [1, 2, 3]
    })

    validate_duplicate_orders(data)


def test_validate_duplicate_orders_failure():

    data = pd.DataFrame({
        "order_id": [1, 1, 2]
    })

    with pytest.raises(ValueError):
        validate_duplicate_orders(data)