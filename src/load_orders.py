import pandas as pd
from database import get_connection

# Read CSV
df = pd.read_csv("data/bronze/orders.csv")
print(df.columns)
print(df.columns.tolist())

# Connect to MySQL
connection = get_connection()

# Create cursor
cursor = connection.cursor()

# Insert rows
for index, row in df.iterrows():
    cursor.execute(                  #this cursor.execute sends sql commands to mysql from here
        """
        INSERT INTO orders
        (order_id, customer_name, product, price, order_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            row["order_id"],
            row["customer_name"],
            row["product"],
            row["price"],
            row["order_date"]
        )
    )

# Save changes
connection.commit()

print("Data inserted successfully!")

cursor.close()
connection.close()