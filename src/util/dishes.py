import json

from util.inventory import InventoryManager


class Dish:
    dishName: str
    items: list[str] # List of InventoryItem names
    price: float
    recipe: list[str]
    currentDiscount: float

    def __init__(self, dishName: str, items: list[str], price: float, recipe: list[str]):
        self.dishName = dishName
        self.items = items
        self.price = price
        self.recipe = recipe
        self.currentDiscount = 0

    def get_price(self):
        return self.price - (self.price * self.currentDiscount)

class DishEncoder(json.JSONEncoder):
    def default(self, o: Dish):
        return o.__dict__

def decode_dish(obj: dict) -> Dish:
    dish = Dish(obj["dishName"], obj["items"], obj["price"], obj["recipe"])
    dish.currentDiscount = obj["currentDiscount"]
    return dish

class DishManager:
    dishes: list[Dish]

    def __init__(self):
        self.dishes = []
        self.load()

    def save(self):
        with open("dishes.json", "w") as file:
            json.dump(self.dishes, file, indent = 4, cls = DishEncoder)

    def load(self):
        try:
            with open("dishes.json", "r") as file:
                data = json.load(file, object_hook = decode_dish)
                self.dishes = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def get_dish(self, name: str) -> Dish | None:
        for item in self.dishes:
            if item.dishName == name:
                return item

        return None

    # Similar to get_dish, except is case-insensitive.
    def get_dish_lenient(self, name: str) -> Dish | None:
        for dish in self.dishes:
            if dish.dishName.lower().strip() == name.lower().strip():
                return dish

        return None

    # Check if a dish is available by iterating through the inventory and
    # seeing if there is enough of the item.
    def is_dish_available(self, dish: Dish) -> bool:
        inventory = InventoryManager()
        items = {}

        # It's possible to have multiple of the same item in the list,
        # so count them and assign them to a dict with the item name as the key,
        # and the amount as the value.
        for itemName in dish.items:
            if items[itemName] is not None:
                items[itemName] = items[itemName] + 1
            else:
                items[itemName] = 1

        # Check if there are enough of every item in the inventory.
        for itemName in items:
            amount = items[itemName]
            item = inventory.get_item(itemName)

            if item.amount < amount:
                return False

        return True