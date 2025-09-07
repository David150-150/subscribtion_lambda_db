# -------------Import the Required Libraries-----------#
import os

import mysql.connector
from dotenv import load_dotenv

# -------------Load Env Variables---------#
load_dotenv()


# -------------Reusable Lambda-like Function-------#
def lambda_handler(event=None, context=None):
    tables_to_test = [
        "customer",
        "product",
        "subscription",
        "transaction",
        "transaction_details",
        "transaction_failures",
        "schedule",
    ]

    results = {}

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        cursor = connection.cursor(dictionary=True)

        for table in tables_to_test:
            try:
                cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
                results[table] = cursor.fetchall()
            except mysql.connector.Error as e:
                results[table] = f"Query error: {str(e)}"

        return {"statusCode": 200, "body": results}

    except mysql.connector.Error as err:
        return {"statusCode": 500, "body": f"Database error: {str(err)}"}

    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals() and connection.is_connected():
            connection.close()


# -------------Optional Test Function Locally----------#
if __name__ == "__main__":
    from pprint import pprint

    pprint(lambda_handler({}, {}))


# -------------Wrapper for FastAPI Endpoint------------#
def get_summary_data():
    result = lambda_handler({}, {})
    return {"status": "success", "data": result["body"]}
