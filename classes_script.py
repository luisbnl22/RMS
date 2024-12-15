


class MenuItem:
    def __init__(self, name: str, item_type: str, price: float, availability: bool):
        """
        Represents a menu item in restaurant's menu.

        Parameters:
        name (str): The name of the menu item.
        item_type (str): The type of item (e.g., 'starter', 'main', 'dessert').
        price (float): The price of the menu item.
        availability (bool): Availability of the item (True for available, False for unavailable).
        """
        self.name = name
        self.item_type = item_type
        self.price = price
        self.availability = availability



class Accesses:
    def __init__():
        # Check login state
        if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
            # Stop unauthorized access and hide the page content
            st.warning("You must log in to access this page.")
            st.stop()

        # If authenticated, page content starts here
        st.sidebar.success(f"Logged in as: {st.session_state['role']}")
        st.title("Page 1")
        st.write("This content is only visible to authenticated users.")