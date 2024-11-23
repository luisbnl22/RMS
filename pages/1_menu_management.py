import streamlit as st
import pandas as pd 
from database import db_setup
from classes_script import MenuItem


# Initialize session state to track if the popup should appear
if "show_popup" not in st.session_state:
    st.session_state["show_popup"] = False

# Function to toggle the popup
def toggle_popup():
    st.session_state["show_popup"] = not st.session_state["show_popup"]


# "Add Option" button
if st.button("Add Option"):
    toggle_popup()  # Show the popup

# Popup-like behavior
# if st.session_state["show_popup"]:
#     st.write("### Add a New Menu Option")
#     # Text input for the new option
#     new_option = st.text_input("Enter the name of the new option:")
#     add_button = st.button("Confirm Add")  # Button to confirm the addition
#     cancel_button = st.button("Cancel")   # Button to cancel

#     if add_button and new_option:
#         st.success(f"Option '{new_option}' has been added!")
#         # Reset popup state after adding
#         st.session_state["show_popup"] = False

#     elif cancel_button:
#         st.info("Addition canceled.")
#         # Reset popup state after canceling
#         st.session_state["show_popup"] = False


if not st.session_state["show_popup"]:

    raw_data = db_setup.fetch_query("SELECT * FROM menu where type = 'Food'")

    menu = []
    for iter in raw_data:
        menu.append([iter[1],iter[4]])
        #NOME E DISPONIBILIDADE

    # Create a dictionary to store the state of each menu item
    menu_state = {}

    # Display options for "Food"
    st.title("Food")
    for food in menu:
        # Add a checkbox for each food item
        menu_state[food[0]] = st.checkbox(food[0], value=food[1])  # Default: selected

    # Add a separator
    st.markdown("---")

    raw_data_bebidas = db_setup.fetch_query("SELECT * FROM menu where type = 'Beverage'")

    menu_bebidas = []
    for iter in raw_data_bebidas:
        menu_bebidas.append([iter[1],iter[4]])

    # Display options for "Drinks"
    st.title("Drinks")
    for drink in menu_bebidas:
        # Add a checkbox for each drink item
        menu_state[drink[0]] = st.checkbox(drink[0], value=drink[1])  # Default: selected

    # Add a save button
    if st.button("Save Changes"):
        # Confirmation warning
        st.warning("Are you sure you want to save the changes?")

        # Confirmation and cancel buttons
        confirm = st.button("Confirm")
        cancel = st.button("Cancel")

        if confirm:
            activated = [item for item, state in menu_state.items() if state]
            deactivated = [item for item, state in menu_state.items() if not state]

            for i in deactivated:
                print("O que e o i:")
                print(i)
                db_setup.execute_query("update menu set availability = 0 where name = '?'",(i,))

        elif cancel:
            st.info("Changes have been discarded.")
else:
    # Popup UI
    st.write("### Add a New Menu Option")
    
    INPUTname = st.text_input("Enter the name of the new option:")
    INPUTtype = st.selectbox("Type",['Food','Beverage'])
    INPUTprice = st.number_input("Insert price of product")
    INPUTavailability = st.number_input("Availability (0-NO,1-YES)",min_value=0,max_value=1,step=1)


    add_button = st.button("Confirm Add")
    cancel_button = st.button("Cancel")

    if add_button and INPUTname:
        
        item = MenuItem(INPUTname,INPUTtype,INPUTprice,INPUTavailability)
        db_setup.insert_menu_product(item)

        #st.success(f"Option '{new_option}' has been added!")
        st.session_state["show_popup"] = False  # Close popup after adding

    elif cancel_button:
        st.info("Addition canceled.")
        st.session_state["show_popup"] = False  # Close popup after canceling