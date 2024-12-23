import sqlite3
import os
import pathlib
import pandas as pd
import datetime as dt



class Database:
    def __init__(self):
        SCRIPT_DIR = pathlib.Path(__file__).parent.parent
        
        self.db_path = SCRIPT_DIR / "data" / "restaurant.db"

        self.file_path = SCRIPT_DIR / "database" / "initial_files" / "data.xlsx"

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=()):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()

    def fetch_query(self, query, params=(), single_output = False):
        with self.connect() as connection:
            if single_output == False:
                cursor = connection.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
            elif single_output == True:
                results = self.fetch_query(query, params)
                return [row[0] for row in results]

    def recreate_db(self):
        db_path = self.db_path

        # Remove existing database file (optional, ensures a clean start)
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database at {db_path}")

        self.execute_query("""
        CREATE TABLE IF NOT EXISTS menu(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            availability INTEGER DEFAULT 1,
            cost REAL NOT NULL
        );
        """)

        cwd_file = self.file_path

        menu = pd.read_excel(cwd_file,sheet_name = 'menu')

        menu.to_sql("menu", self.connect(), if_exists="append", index=False)

        #TABLES TABLE

        self.execute_query("""
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capacity INTEGER NOT NULL,
            is_occupied INTEGER DEFAULT 0
        );
        """)


        tables = pd.read_excel(cwd_file,sheet_name = 'tables')

        tables.to_sql("tables", self.connect(), if_exists="append", index=False)

        #ORDERS TABLE
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantity INT NOT NULL,
            order_time DATETIME NOT NULL,
            status TEXT DEFAULT 'Pending',
            finish_time DATETIME 
        );
        """)

        print(f"Empty database created at {db_path}")        

class MenuManagement:
    def __init__(self):
        self.db = Database()
    
    def insert_menu_product(self,product_obj):

        params =  (product_obj.name,product_obj.item_type,product_obj.price,product_obj.availability)

        self.db.execute_query("insert into menu(name,type,price,availability) values (?,?,?,?,?))",params)

class OrderManagement:
    def __init__(self):
        self.db = Database()

    @staticmethod
    def GENERATE_order_df():
        return pd.DataFrame(columns=['item','quantity'])

    @staticmethod
    def ADD_order_df(original_df,new_item,new_quantity):
    
        new_df = pd.DataFrame({'item':[new_item],'quantity':[new_quantity]})

        original_df = pd.concat([original_df,new_df])

        return original_df
    
    def ADD_order_df_to_db(self,df,table_number):
        
        df['table_id'] = table_number
        df['order_time'] = dt.datetime.now()


        df.to_sql("orders", self.db.connect(), if_exists="append", index=False)

        table_number = table_number.split("-")[0]

        self.db.execute_query(f"update tables set is_occupied = 1 where id = {table_number}")


class DataInteraction:  
    def __init__(self):
        self.db = Database()

    def GET_available_tables(self):
        self.db.fetch_query("""SELECT id || ' - ' || capacity || ' capacity'
                            FROM tables
                            WHERE is_occupied = 0;
                        """,single_output = True)

    def GET_available_food(self):
        self.db.fetch_query(""" 
                SELECT name FROM menu 
                where type = 'Food' and availability = 1
                """,
                single_output = True
                )  

    def GET_available_drink(self):
        self.db.fetch_query("""
            SELECT name FROM menu where type = 'Beverage' 
            and availability = 1""",single_output = True)  

    def GET_week_sales(self):

        df_init = self.db.fetch_query("SELECT item, count(*) FROM orders group by item order by count(*) desc")  

        df = pd.DataFrame(df_init)

        df.columns = ['Item','Count']

        return df

    def GET_week_hour_day_sales(self):

        df_init = self.db.fetch_query("""SELECT item, order_time 
                                FROM orders
                            """)  

        df = pd.DataFrame(df_init)

        df.columns = ['Item','Datetime']

        return df

    def GET_orders_df(self, status = ""):
        if status == "":
            df_init = self.db.fetch_query("SELECT * FROM orders")  
        else:
            df_init = self.db.fetch_query(f"SELECT * FROM orders where status = '{status}'")  

        df = pd.DataFrame(df_init)

        if df.empty == False:

            df.columns = ['id','Table','Item','Quantity','order_time','Status','Finish Time']

            df['Minutes since request'] = df['order_time'].apply(utils_time_diff)

            #df = df.drop("id",axis=1)

            df['dense_rank'] = df['order_time'].rank(method='dense', ascending=True)

        return df
    
class TableManagement:  
    def __init__(self):
        self.db = Database()

    def POST_finish_order(self, id):

        params = (id)
        self.db.execute_query("update orders set status = 'Completed' where id = ?",params=params)

        date_now_str = dt.datetime.now()

        self.db.execute_query(f"update orders set finish_time = '{date_now_str}' where id = {id}")







