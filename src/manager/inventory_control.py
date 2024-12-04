from util.accounts import Account
from util.dishes import DishManager
from util.inventory import InventoryManager
from util.menu import OptionMenu
from util.pagination import create_pagination


# Dishes inventory
def display_dishes(dishManager: DishManager, page: int):
    create_pagination(dishManager, "Dish Inventory Control", dishManager.dishes, (lambda dish: f"{dish.dishName} - ${dish.price}"), None, page)

# Ingredients inventory
def display_inventory(inventoryManager: InventoryManager, page: int):
    create_pagination(inventoryManager, "Ingredient Inventory Control", inventoryManager.items, (lambda item: f"{item.itemName} - {item.amount} units"), None, page)

def init(account: Account):
    inventoryManager = InventoryManager()
    dishManager = DishManager()

    controlMenu = OptionMenu("Inventory Control")
    controlMenu.description = "In this menu, you can view, update, add and remove items in the inventory."
    controlMenu.description += "\nSelect which inventory you would like to perform actions on."

    controlMenu.add_option("Dishes", lambda: display_dishes(dishManager, 0))
    controlMenu.add_option("Ingredients", lambda: display_inventory(inventoryManager, 0))

    controlMenu.process()

    pass