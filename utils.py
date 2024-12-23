import streamlit as st



class Utils:
    @staticmethod
    def minute_diff(request_date):
        """
        Receives date in string format and returns minutes passed since that date in minutes int
        """
        now = dt.datetime.now()

        date_object = dt.datetime.strptime(request_date, "%Y-%m-%d %H:%M:%S.%f")

        diff_sec = (now-date_object).seconds
        diff_minutes = int(diff_sec/60)

        return diff_minutes


class AccessManagement:
    def __init__(self):
        # Initialize session state variables if they do not exist
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
        if "role" not in st.session_state:
            st.session_state["role"] = "Guest"
        if "show_popup" not in st.session_state:
            st.session_state["show_popup"] = False
    
    def check_authentication(self):
        """Check if the user is authenticated. If not, show a warning and stop the app."""
        if not st.session_state["authenticated"]:
            st.warning("You must log in to access this page.")
            st.stop()

    def display_sidebar(self):
        """Display the sidebar with the logged-in user information."""
        st.sidebar.success(f"Logged in as: {st.session_state['role']}")

    def display_page_header(self):
        """Display the title and header for the page content."""
        st.title("Page 1")
        st.write("This content is only visible to authenticated users.")

    def initialize_popup_state(self):
        """Initialize session state to track if the popup should appear."""
        if "show_popup" not in st.session_state:
            st.session_state["show_popup"] = False

    def toggle_popup(self):
        """Function to toggle the popup visibility."""
        st.session_state["show_popup"] = not st.session_state["show_popup"]


