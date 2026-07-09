import pandas as pd

orders = pd.DataFrame(
    {
        "order_id": [101, 102, 102, 103, 104, 105],
        "customer_name": ["Bhanu", " Ravi ", " Ravi ", "ARJUN", None, "Kiran"],
        "product": ["Laptop", "Mouse", "Mouse", "Keyboard", "Monitor", None],
        "price": [80000, 500, 500, 1200, 25000, 7000]
    }
)

orders.to_csv("data/raw/orders.csv", index=False)

print("Raw data created successfully!")