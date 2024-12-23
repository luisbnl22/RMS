import random
import pandas as pd
from datetime import datetime, timedelta

# Menu items
menu = [
    ("Water", "Beverage", 1, 0.6),
    ("Coca cola", "Beverage", 1, 0.7),
    ("Pepsi", "Beverage", 1, 0.7),
    ("Fried fish", "Food", 10, 4),
    ("Lasagna", "Food", 8, 3),
    ("Pizza Margherita", "Food", 6, 2.5),
    ("Pizza Bacon", "Food", 7, 2.5),
    ("Chicken breast", "Food", 10, 3)
]

# Tables availability
tables = [
    (10, 0),
    (10, 0),
    (10, 0),
    (5, 0),
    (5, 0),
    (5, 0),
    (2, 0),
    (2, 0),
    (2, 0)
]

# Function to generate random orders for the week
def generate_orders(num_rows=30):
    orders = []
    today = datetime.now()
    for _ in range(num_rows):  # Generate 30 orders
        table_id = random.randint(1, len(tables))  # Random table ID
        item = random.choice(menu)[0]  # Random item from menu
        quantity = random.randint(1, 5)  # Random quantity
        order_time = today + timedelta(days=random.randint(0, 6), hours=random.randint(10, 22), minutes=random.randint(0, 59))
        finish_time = order_time + timedelta(minutes=random.randint(15, 45))  # Random finish time after the order
        status = "Pending"
        
        order = {
            'table_id': table_id,
            'item': item,
            'quantity': quantity,
            'order_time': order_time,
            'status': status,
            'finish_time': finish_time
        }
        orders.append(order)
    
    return pd.DataFrame(orders)

# Generate the orders DataFrame with 30 rows
orders_df = generate_orders(500)

# Display the first few rows
orders_df.to_excel("tt.xlsx")
