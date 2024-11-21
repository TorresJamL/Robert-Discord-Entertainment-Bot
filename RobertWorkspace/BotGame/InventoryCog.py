### Inventory Class
from ItemsCog import *

class Inventory():
    def __init__(self, size: int) -> None:
        self.size = size
        self.inventory = []

    def __str__(self) -> str:
        L = ""
        for item in self.inventory:
            L += str(item) + "\n"
        return L

    def get_size(self):
        """Returns inventory size
        """
        return self.size
    
    def is_empty(self):
        """Returns true if inventory is empty, false otherwise
        """
        return self.inventory == []

    def percent_used(self):
        """returns the precent of the inventory used
        """
        return int((len(self.inventory) / self.size) * 100)

    def grow(self, amount: int = 1):
        """Grows the inventory capacity
        Args:
            amount (int, optional): How much to grow the inventory by. Defaults to 1.
        """
        self.size += amount

    def shrink(self, amount: int = 1):
        """Shrinks the inventory capacity
        Args:
            amount (int, optional): How much to shrink the inventory by. Defaults to 1.
        """
        self.size -= amount

    def add_item(self, item: Item):
        """Adds an item to an inventory. Returns a string only if inventory is full.
        Args:
            item (Item): The item to be added to the inventory.
        Returns: "Inventory full"
        """
        if self.percent_used() < 100:
            self.inventory += [item]
        else:
            return "Inventory full"

    def remove_item(self, item: Item):
        """Removes an item from the inventory
        Args:
            item (Item): An item in the inventory
        Returns:
            Returns "Inventory is already empty." if inventory is empty, \n
            "Item could not be found." if the item could not be found, \n 
            Nothing if an item was removed successfully.
        """
        if self.is_empty():
            return "Inventory is already empty."
        elif item in self.inventory:
            self.inventory.remove(item)
        else:
            return "Item could not be found."

    def use_item(self, item: Item):
        """Uses an item in the inventory, reduces it's durability.
        Args:
            item (Item): Item to be used. Reduces durability by 1.
        Returns:
            str : Returns empty string if item is removed, \n
            otherwise returns "Item {item}, could not be found."
        """
        if item in self.inventory:
            item = item # re-define 'item' from the parameter so VSC recognizes it's type.
            should_delete = item.lose_durability()
            if should_delete:
                self.remove_item(item)
                return ""
            return str(item)
        else:
            return f"Item: {item}, could not be found."

    def get_items(self, filterType):
        return list(filter(lambda x: type(x) == filterType, self.inventory))
    
    def has_item(self, item: Item):
        return True if item in self.inventory else False