import streamlit as st
import pandas as pd 
from database import db_setup
from classes_script import MenuItem
import logging
import pdb
import time


# Initialize session state to track if the popup should appear
if "show_popup" not in st.session_state:
    st.session_state["show_popup"] = False

# Function to toggle the popup
def toggle_popup():
    st.session_state["show_popup"] = not st.session_state["show_popup"]


# "Add Option" button
if st.button("Add new Menu Option"):
    toggle_popup()  # Show the popup

st.markdown("---")


st.title("Existing Options")

if not st.session_state["show_popup"]:


    raw_data = db_setup.fetch_query("SELECT name, availability FROM menu where type = 'Food'")


    #st.write(raw_data)
    menu = []
    for iter in raw_data:
        menu.append([iter[0],iter[1]])
        #NOME E DISPONIBILIDADE

    # Initialize session state for menu_state
    if "menu_state" not in st.session_state:
        st.session_state.menu_state = {}

    # # Create a dictionary to store the state of each menu item
    # menu_state = {}

    # Display options for "Food"
    st.title("Food")
    for food in menu:
        # Add a checkbox for each food item
        st.session_state.menu_state[food[0]] = st.checkbox(food[0], value=st.session_state.get(food[0],food[1]))  # Default: selected

    # Add a separator
    st.markdown("---")

    raw_data_bebidas = db_setup.fetch_query("SELECT name, availability FROM menu where type = 'Beverage'")

    menu_bebidas = []
    for iter in raw_data_bebidas:
        menu_bebidas.append([iter[0],iter[1]])




    

    # Display options for "Drinks"
    st.title("Drinks")
    for drink in menu_bebidas:
         st.session_state.menu_state[drink[0]] = st.checkbox(
        drink[0], value=st.session_state.menu_state.get(drink[0], drink[1])
        )
         
    # for food in menu:
    #     st.session_state.menu_state[food[0]] = st.checkbox(
    #     food[0], value=st.session_state.menu_state.get(food[0], food[1])
    # )

    # Add a save button
    # Add a save button
    if st.button("Save Changes"):
       

        #PRODUCTS TO DEACTIVATE
        deactivated_names = [
            item for item, state in st.session_state.menu_state.items() if not state
        ]

        if deactivated_names:
            #st.write(f"Deactivating: {deactivated_names}")

            deactivated_names_tuple = tuple(deactivated_names)

            if len(deactivated_names)==1:                
                deactivated_names_tuple = str(deactivated_names_tuple).replace(',','')
            else:
                deactivated_names_tuple = str(deactivated_names_tuple)

            #st.write(f"UPDATE menu SET availability = 0 WHERE name IN {deactivated_names_tuple}")
            
            db_setup.execute_query(f"UPDATE menu SET availability = 0 WHERE name IN {deactivated_names_tuple}")

        #PRODUCTS TO ACTIVATE

        activated_names = [
            item for item, state in st.session_state.menu_state.items() if state is True]

        #st.write(activated_names)

        if activated_names:

            activated_names_tuple = tuple(activated_names)

            if len(activated_names)==1:                
                activated_names_tuple = str(activated_names_tuple).replace(',','')
            else:
                activated_names_tuple = str(activated_names_tuple)

            #st.write(f"UPDATE menu SET availability = 1 WHERE name IN {activated_names_tuple}")
            
            db_setup.execute_query(f"UPDATE menu SET availability = 1 WHERE name IN {activated_names_tuple}")

        st.success("Changes saved successfully.")
        st.session_state.show_confirmation = False

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