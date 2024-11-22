import streamlit as st
import pandas as pd

# Define menu options for categories
menu = {
    "Food": ["Pizza", "Burger", "Pasta", "Salad", "Soup"],
    "Drinks": ["Water", "Soda", "Juice", "Beer", "Wine"]
}

# Create a dictionary to store the state of each menu item
menu_state = {}

# Display options for "Food"
st.title("Food")
for food in menu["Food"]:
    # Add a checkbox for each food item
    menu_state[food] = st.checkbox(food, value=True)  # Default: selected

# Add a separator
st.markdown("---")

# Display options for "Drinks"
st.title("Drinks")
for drink in menu["Drinks"]:
    # Add a checkbox for each drink item
    menu_state[drink] = st.checkbox(drink, value=True)  # Default: selected

# Add a save button
if st.button("Save Changes"):
    # Confirmation warning
    st.warning("Are you sure you want to save the changes?")

    # Confirmation and cancel buttons
    confirm = st.button("Confirm")
    cancel = st.button("Cancel")

    if confirm:
        st.success("Changes have been saved!")
        # Display the activated and deactivated options
        st.write("Here are the current selections:")
        activated = [item for item, state in menu_state.items() if state]
        deactivated = [item for item, state in menu_state.items() if not state]
        st.write(f"**Activated:** {', '.join(activated)}")
        st.write(f"**Deactivated:** {', '.join(deactivated)}")
    elif cancel:
        st.info("Changes have been discarded.")
