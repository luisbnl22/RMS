import streamlit as st
import pandas as pd
from database import db_setup
import utils as utils

ui = utils.AccessManagement()
OrderManagement = db_setup.OrderManagement()
db = db_setup.Database()
DataInteraction = db_setup.DataInteraction()


ui.check_authentication()
ui.display_sidebar()
ui.display_page_header()
ui.initialize_popup_state()


# Get customer details before selecting menu items
st.title("Order Management")

# Customer Details Inputs
table_number = st.selectbox("Table Number",DataInteraction.GET_available_tables())
person_name = st.text_input("Person's Name")

# Only proceed if both fields are filled
if table_number and person_name:
    # Create a list to store selected items and their quantities
    order = OrderManagement.GENERATE_order_df()

    # Display options for "Food"
    st.subheader("Select Food Items")
    menu = DataInteraction.GET_available_food()

    for food in menu:
        # Add checkbox for each food item
        selected = st.checkbox(food, key=food)
        if selected:
            # Allow user to input quantity
            quantity = st.number_input(f"Quantity for {food}", min_value=0, step=1, key=f"quantity_{food}")
            if quantity > 0:
                
                order = OrderManagement.ADD_order_df(order,food,quantity)
                

    # Add a separator
    st.markdown("---")

    menu_drinks = DataInteraction.GET_available_drink()

    # Display options for "Drinks"
    st.subheader("Select Drink Items")
    for drink in menu_drinks:
        # Add checkbox for each drink item
        selected = st.checkbox(drink, key=drink)
        if selected:
            # Allow user to input quantity
            quantity = st.number_input(f"Quantity for {drink}", min_value=0, step=1, key=f"quantity_{drink}")
            if quantity > 0:
                order = OrderManagement.ADD_order_df(order,drink,quantity)

    #st.write(order)

    # Display the order summary before submission
    if order.empty is False:
        st.subheader("Your Order Summary")
        # Create a DataFrame from the order list
        #df_order = pd.DataFrame(order)
        #st.dataframe(order)

        # Submit button for finalizing the order
        if st.button("Submit Order"):
            OrderManagement.ADD_order_df_to_db(order,table_number)
            st.success("Order submitted successfully!")
    else:
        st.write("No items selected yet.")
else:
    st.warning("Please enter the table number and the person's name to proceed.")
