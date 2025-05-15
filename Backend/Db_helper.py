import mysql.connector
from mysql.connector import Error

# Connection helper
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Green@2024",
        database="pandeyji_eatery"
    )

# ✅ Insert order item using stored procedure
def insert_order_item(food_item, quantity, order_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        connection.commit()
        print("Order item inserted successfully!")
        return 1
    except Error as err:
        print(f"Error inserting order item: {err}")
        connection.rollback()
        return -1
    finally:
        cursor.close()
        connection.close()

# ✅ Insert into order_tracking
def insert_order_tracking(order_id, status):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(query, (order_id, status))
        connection.commit()
        print("Order tracking inserted!")
        return 1
    except Error as err:
        print(f"Error inserting order tracking: {err}")
        connection.rollback()
        return -1
    finally:
        cursor.close()
        connection.close()

# ✅ Get total order price from stored function
def get_total_order_price(order_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT get_total_order_price({order_id})")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Error as err:
        print(f"Error fetching order price: {err}")
        return 0
    finally:
        cursor.close()
        connection.close()

# ✅ Get next order_id
def get_next_order_id():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(order_id) FROM orders")
        result = cursor.fetchone()
        return (result[0] or 0) + 1
    except Error as err:
        print(f"Error fetching next order ID: {err}")
        return 1
    finally:
        cursor.close()
        connection.close()

# ✅ Get order status
def get_order_status(order_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT status FROM order_tracking WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as err:
        print(f"Error fetching order status: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def clear_order_session(session_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="your_database"
    )
    cursor = conn.cursor()
    try:
        # You can adjust the table name and conditions based on your schema
        cursor.execute("DELETE FROM orders WHERE session_id = %s", (session_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
        
# # ✅ Get item_id from items table
# def get_item_id_by_name(food_name):
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#         cursor.execute("SELECT id FROM items WHERE name = %s", (food_name,))
#         result = cursor.fetchone()
#         return result[0] if result else None
#     except Error as err:
#         print(f"Error getting item ID for '{food_name}': {err}")
#         return None
#     finally:
#         cursor.close()
#         connection.close()
