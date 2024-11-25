import streamlit as st
import pandas as pd
from database import db_setup

# Get customer details before selecting menu items
st.title("Order Management")

# Customer Details Inputs
table_number = st.selectbox("Table Number",db_setup.GET_available_tables())
person_name = st.text_input("Person's Name")

# Only proceed if both fields are filled
if table_number and person_name:
    # Create a list to store selected items and their quantities
    order = db_setup.GENERATE_order_df()

    # Display options for "Food"
    st.subheader("Select Food Items")
    menu = db_setup.GET_available_food()

    for food in menu:
        # Add checkbox for each food item
        selected = st.checkbox(food, key=food)
        if selected:
            # Allow user to input quantity
            quantity = st.number_input(f"Quantity for {food}", min_value=0, step=1, key=f"quantity_{food}")
            if quantity > 0:
                
                order = db_setup.ADD_order_df(order,food,quantity)
                

    # Add a separator
    st.markdown("---")

    menu_drinks = db_setup.GET_available_drink()

    # Display options for "Drinks"
    st.subheader("Select Drink Items")
    for drink in menu_drinks:
        # Add checkbox for each drink item
        selected = st.checkbox(drink, key=drink)
        if selected:
            # Allow user to input quantity
            quantity = st.number_input(f"Quantity for {drink}", min_value=0, step=1, key=f"quantity_{drink}")
            if quantity > 0:
                order = db_setup.ADD_order_df(order,drink,quantity)

    st.write(order)

    # Display the order summary before submission
    if order:
        st.subheader("Your Order Summary")
        # Create a DataFrame from the order list
        df_order = pd.DataFrame(order)
        st.dataframe(df_order)

        # Submit button for finalizing the order
        if st.button("Submit Order"):
            st.write(f"**Order for Table {table_number}**")
            st.write(f"**Customer: {person_name}**")
            st.dataframe(df_order)
            st.success("Order submitted successfully!")
    else:
        st.write("No items selected yet.")
else:
    st.warning("Please enter the table number and the person's name to proceed.")
