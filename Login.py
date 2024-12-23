import streamlit as st
import hashlib

# User credentials
USER_CREDENTIALS = {
    "admin": [hashlib.sha256("admin123".encode()).hexdigest(), "admin"],
    "staff": [hashlib.sha256("staff123".encode()).hexdigest(), "staff"],
    "viewer": [hashlib.sha256("viewer123".encode()).hexdigest(), "viewer"]
}

# Function to authenticate users
def authenticate(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username][0] == hashed_pw:
        return USER_CREDENTIALS[username][1]  # Return role
    return None

# Login state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = None

# If not authenticated
if not st.session_state["authenticated"]:
    st.title("Login")
    username = st.text_input("Username", "")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        role = authenticate(username, password)
        if role:
            st.session_state["authenticated"] = True
            st.session_state["role"] = role
            st.success(f"Welcome, {username}! Redirecting...")
            #st.experimental_rerun()
        else:
            st.error("Invalid username or password. Please try again.")
else:
    # Only show navigation/sidebar if authenticated
    st.sidebar.success(f"Logged in as: {st.session_state['role']}")
    st.sidebar.write("Use the navigation to access other pages.")
    st.write("Welcome to the main dashboard!")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.experimental_rerun()
