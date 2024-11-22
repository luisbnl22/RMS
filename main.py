import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Custom Sidebar",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# Sidebar navigation using page links
with st.sidebar:
    st.header("Navigation")
    # Using st.page_link() to navigate between pages
    st.page_link("Dashboard")
    st.page_link("Menu Management")
    st.page_link("Table Management")
    st.page_link("Order Management")

# Display the current page content based on the session state
if st.session_state["current_page"] == "Dashboard":
    st.title("Welcome to the Dashboard")
    st.write("This is the Dashboard page.")
elif st.session_state["current_page"] == "Menu Management":
    st.title("Menu Management")
    st.write("This is the Menu Management page.")
elif st.session_state["current_page"] == "Table Management":
    st.title("Table Management")
    st.write("This is the Table Management page.")
elif st.session_state["current_page"] == "Order Management":
    st.title("Order Management")
    st.write("This is the Order Management page.")
