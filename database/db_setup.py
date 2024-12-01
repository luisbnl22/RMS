import sqlite3
import os
#from database import db_setup

import pandas as pd
import datetime as dt

def utils_time_diff(request_date):
    now = dt.datetime.now()

    date_object = dt.datetime.strptime(request_date, "%Y-%m-%d %H:%M:%S.%f")

    diff_sec = (now-date_object).seconds
    diff_minutes = int(diff_sec/60)

    return diff_minutes



def create_database():
    # Get the parent directory of the current script
    # Get the relative parent directory (one level up)
    parent_dir = os.path.join(os.getcwd())

    # Path for the database in the parent folder
    db_path = os.path.join(parent_dir, "data", "restaurant.db")

    # Ensure the "data/" directory exists in the parent folder
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Remove existing database file (optional, ensures a clean start)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")


    # Create a new empty database and define schema
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create empty tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        availability INTEGER DEFAULT 1
    );
    """)

    cwd = os.getcwd()
    cwd = cwd + '\\database\\initial_files\\data.xlsx'
    cwd = cwd.replace("\\","/")

    menu = pd.read_excel(cwd,sheet_name = 'menu')

    menu.to_sql("menu", connection, if_exists="append", index=False)

    #TABLES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        capacity INTEGER NOT NULL,
        is_occupied INTEGER DEFAULT 0
    );
    """)


    data = pd.read_excel(cwd,sheet_name = 'tables')

    data.to_sql("tables", connection, if_exists="append", index=False)


    #ORDERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        quantity INT NOT NULL,
        order_time DATETIME NOT NULL,
        status TEXT DEFAULT 'Pending'
    );
    """)

    # Commit and close connection
    connection.commit()
    connection.close()

    print(f"Empty database created at {db_path}")

def execute_query(query, params=()):
    connection = sqlite3.connect("data/restaurant.db")
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()

def fetch_query(query, params=()):
    connection = sqlite3.connect("data/restaurant.db")
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()

    #rows = [row[0] for row in cursor.fetchall()]
    connection.close()
    return rows

def fetch_query_single_output(query, params=()):
    connection = sqlite3.connect("data/restaurant.db")
    cursor = connection.cursor()
    cursor.execute(query, params)
    #rows = cursor.fetchall()

    rows = [row[0] for row in cursor.fetchall()]
    connection.close()
    return rows

def insert_menu_product(product_obj):
    connection = sqlite3.connect("data/restaurant.db")
    cursor = connection.cursor()

    query = f"insert into menu(name,type,price,availability) values ('{product_obj.name}','{product_obj.item_type}','{product_obj.price}','{product_obj.availability}')"

    cursor.execute(query)
    connection.commit()
    connection.close()

def GET_available_tables():
    return fetch_query_single_output("""SELECT id || ' - ' || capacity || ' capacity'
                        FROM tables
                        WHERE is_occupied = 0;
                       """)

    
def GET_available_food():
    return fetch_query_single_output(""" SELECT name FROM menu where type = 'Food' and availability = 1""")  

def GET_available_drink():
    return fetch_query_single_output(""" SELECT name FROM menu where type = 'Beverage' and availability = 1""")  

def GET_orders_df():
    df_init = fetch_query("SELECT * FROM orders")  

    df = pd.DataFrame(df_init)

    df.columns = ['id','Table','Item','Quantity','order_time','Status']

    df['Minutes since request'] = df['order_time'].apply(utils_time_diff)

    df = df.drop("id",axis=1)

    df['dense_rank'] = df['order_time'].rank(method='dense', ascending=True)
    #df = df.drop("order_time",axis=1)

    #df.columns = ['id','Table','Item','Quantity','Order time','Status']

    return df





def GENERATE_order_df():
    return pd.DataFrame(columns=['item','quantity'])

def ADD_order_df(original_df,new_item,new_quantity):
    
    new_df = pd.DataFrame({'item':[new_item],'quantity':[new_quantity]})

    original_df = pd.concat([original_df,new_df])

    return original_df

def ADD_order_df_to_db(df,table_number):
    
    connection = sqlite3.connect("data/restaurant.db")
    #cursor = connection.cursor()
    df['table_id'] = table_number
    df['order_time'] = dt.datetime.now()


    df.to_sql("orders", connection, if_exists="append", index=False)
    #connection.commit()
    #connection.close()

    table_number = table_number.split("-")[0]

    execute_query(f"update tables set is_occupied = 1 where id = {table_number}")



if __name__ == "__main__":
    create_database()
 
#print(fetch_query("select * from orders"))



# idd = 5
# execute_query(f"update tables set is_occupied = 1 where id = {idd}")

