import json

class Dish:
    dishName: str
    items: list[str] # List of InventoryItem names
    price: float
    recipe: list[str]

    def __init__(self, dishName: str, items: list[str], price: float, recipe: list[str]):
        self.dishName = dishName
        self.items = items
        self.price = price
        self.recipe = recipe

class DishEncoder(json.JSONEncoder):
    def default(self, o: Dish):
        return o.__dict__

def decode_dish(obj: dict) -> Dish:
    return Dish(obj["dishName"], obj["items"], obj["price"], obj["recipe"])

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
