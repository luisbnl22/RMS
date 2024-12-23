import streamlit as st
import pandas as pd 
from database import db_setup
from classes_script import MenuItem
import logging
import pdb
import time
import utils as utils


ui = utils.AccessManagement()
MenuManagement = db_setup.MenuManagement()
db = db_setup.Database()


ui.check_authentication()
ui.display_sidebar()
ui.display_page_header()
#ui.toggle_popup()


if st.button("Add new Menu Option"):
    ui.toggle_popup()  # Show the popup

if not st.session_state["show_popup"]:
    
    # Initialize session state for menu_state
    if "menu_state" not in st.session_state:
        st.session_state.menu_state = {}

    
    # Display options for "Food"

    menu = MenuManagement.GET_list_options('Food')
    st.title("Food")
    for food in menu:
        st.session_state.menu_state[food[0]] = st.checkbox(food[0], value=st.session_state.get(food[0],food[1])) 

    st.markdown("---")

    menu_bebidas = MenuManagement.GET_list_options('Beverage')

    st.title("Drinks")
    for drink in menu_bebidas:
         st.session_state.menu_state[drink[0]] = st.checkbox(
        drink[0], value=st.session_state.menu_state.get(drink[0], drink[1])
        )
         
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
            
            db.execute_query(f"UPDATE menu SET availability = 0 WHERE name IN {deactivated_names_tuple}")

        #PRODUCTS TO ACTIVATE

        activated_names = [
            item for item, state in st.session_state.menu_state.items() if state is True]

        if activated_names:

            activated_names_tuple = tuple(activated_names)

            if len(activated_names)==1:                
                activated_names_tuple = str(activated_names_tuple).replace(',','')
            else:
                activated_names_tuple = str(activated_names_tuple)
            
            db.execute_query(f"UPDATE menu SET availability = 1 WHERE name IN {activated_names_tuple}")

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
        MenuManagement.insert_menu_product(item)

        st.session_state["show_popup"] = False  # Close popup after adding

    elif cancel_button:
        st.info("Addition canceled.")
        st.session_state["show_popup"] = False  # Close popup after canceling