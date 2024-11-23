


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
