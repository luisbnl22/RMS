import streamlit as st
from database.db_setup import execute_query, fetch_query

# Streamlit app
st.title("Restaurant Management System")

# Tabs for different functionalities
tabs = st.tabs(["Menu Management", "Table Management", "Order Management", "Billing"])

# Menu Management
with tabs[0]:
    st.header("Menu Management")
    menu_items = fetch_query("SELECT * FROM menu")

    # Add menu item
    with st.form("add_menu_item"):
        name = st.text_input("Item Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Add Item")
        if submit and name:
            execute_query("INSERT INTO menu (name, price) VALUES (?, ?)", (name, price))
            st.success("Menu item added!")

    # Display menu
    st.subheader("Current Menu")
    for item in menu_items:
        st.write(f"{item[1]} - ${item[2]:.2f} ({'Available' if item[3] else 'Unavailable'})")

# Table Management
with tabs[1]:
    st.header("Table Management")
    tables = fetch_query("SELECT * FROM tables")

    # Add table
    with st.form("add_table"):
        capacity = st.number_input("Capacity", min_value=1, step=1)
        submit = st.form_submit_button("Add Table")
        if submit:
            execute_query("INSERT INTO tables (capacity) VALUES (?)", (capacity,))
            st.success("Table added!")

    # Display tables
    st.subheader("Current Tables")
    for table in tables:
        status = "Occupied" if table[2] else "Available"
        st.write(f"Table {table[0]} (Capacity: {table[1]}) - {status}")

# Order Management
with tabs[2]:
    st.header("Order Management")
    tables = fetch_query("SELECT * FROM tables WHERE is_occupied = 0")
    menu_items = fetch_query("SELECT * FROM menu WHERE availability = 1")

    # Place an order
    with st.form("place_order"):
        table_id = st.selectbox("Select Table", [t[0] for t in tables])
        order_items = st.multiselect("Select Items", [f"{item[1]} (${item[2]:.2f})" for item in menu_items])
        submit = st.form_submit_button("Place Order")
        if submit:
            item_ids = [menu_items[i][0] for i, item in enumerate(menu_items) if f"{item[1]} (${item[2]:.2f})" in order_items]
            execute_query("INSERT INTO orders (table_id, items) VALUES (?, ?)", (table_id, ",".join(map(str, item_ids))))
            execute_query("UPDATE tables SET is_occupied = 1 WHERE id = ?", (table_id,))
            st.success("Order placed successfully!")

# Billing
with tabs[3]:
    st.header("Billing")
    orders = fetch_query("SELECT * FROM orders WHERE status = 'Pending'")
    for order in orders:
        st.write(f"Order #{order[0]} - Table {order[1]} - Items: {order[2]}")
        total = sum(fetch_query("SELECT price FROM menu WHERE id = ?", (int(item),))[0][0] for item in order[2].split(","))
        st.write(f"Total: ${total:.2f}")
        if st.button(f"Mark Order #{order[0]} as Completed"):
            execute_query("UPDATE orders SET status = 'Completed' WHERE id = ?", (order[0],))
            execute_query("UPDATE tables SET is_occupied = 0 WHERE id = ?", (order[1],))
            st.success(f"Order #{order[0]} completed!")
