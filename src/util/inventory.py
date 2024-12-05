import json

from util.pagination import Manager, ManagerSerializer


class InventoryItem:
    itemName: str
    price: float
    amount: int

    def __init__(self, itemName: str, price: float, amount: int):
        self.itemName = itemName
        self.price = price
        self.amount = amount

def decode_item(obj: dict) -> InventoryItem:
    return InventoryItem(obj["itemName"], obj["price"], obj["amount"])

class InventoryManager(Manager[InventoryItem]):
    items: list[InventoryItem]

    def __init__(self):
        self.items = []
        self.load()

    def save(self):
        with open("inventory.json", "w") as file:
            json.dump(self.items, file, indent = 4, cls = ManagerSerializer)

    def load(self):
        try:
            with open("inventory.json", "r") as file:
                data = json.load(file, object_hook = decode_item)
                self.items = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    # Get an item by its exact name.
    def get_item(self, name: str) -> InventoryItem | None:
        for item in self.items:
            if item.itemName == name:
                return item

        return None

    # Similar to get_item, except is case-insensitive.
    def get_item_lenient(self, name: str) -> InventoryItem | None:
        for item in self.items:
            if item.itemName.lower().strip() == name.lower().strip():
                return item

        return None