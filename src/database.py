import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="bhanu123",
        database="retail_db",
        use_pure=True,
        connection_timeout=5
    )

if __name__ == "__main__":
    print("Inside main")
    try:
        print("Trying to connect...")

        connection = get_connection()

        print("Connection object created")

        if connection.is_connected():
            print("Database Connected Successfully!")

        connection.close()

    except Exception as e:
        print("ERROR:", e)