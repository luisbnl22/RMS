import streamlit as st

# --- Authentication Section ---
def check_authentication():
    """Check if the user is authenticated. If not, show a warning and stop the app."""
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.warning("You must log in to access this page.")
        st.stop()


# --- Sidebar & Page Header Section ---
def display_sidebar():
    """Display the sidebar with the logged-in user information."""
    st.sidebar.success(f"Logged in as: {st.session_state['role']}")

def display_page_header():
    """Display the title and header for the page content."""
    st.title("Page 1")
    st.write("This content is only visible to authenticated users.")

# --- Popup Section ---
def initialize_popup_state():
    """Initialize session state to track if the popup should appear."""
    if "show_popup" not in st.session_state:
        st.session_state["show_popup"] = False

def toggle_popup():
    """Function to toggle the popup visibility."""
    st.session_state["show_popup"] = not st.session_state["show_popup"]