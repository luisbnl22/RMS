import sqlite3
import os
from database import db_setup


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
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        price REAL NOT NULL,
        availability INTEGER DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        capacity INTEGER NOT NULL,
        is_occupied INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        items TEXT NOT NULL,
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
    connection.close()
    return rows

# Initialize the database
if __name__ == "__main__":
    create_database()
 

# create_database()

#execute_query("update menu set availability = 0 where name like '%frang%'")


a = fetch_query("""
   SELECT * FROM menu;
    """)

print(a)

