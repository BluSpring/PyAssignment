import math

from util.accounts import Account
from util.dishes import DishManager
from util.inventory import InventoryManager
from util.menu import OptionMenu


# Dishes inventory
def display_dishes(dishManager: DishManager, page: int):
    maxPages = math.floor(len(dishManager.dishes) / 10)

    # The index to use for printing the orders array
    itemsStart = page * 10

    # Only list up to a max of 10 orders.
    totalDishesToDisplay = min(10, len(dishManager.dishes) - itemsStart)

    productsMenu = OptionMenu(f"Dish Inventory Control")
    productsMenu.automaticallyExit = True
    productsMenu.description = ""

    for i in range(itemsStart, itemsStart + totalDishesToDisplay):
        dish = dishManager.dishes[i]
        productsMenu.description += f"\n  {i + 1}. {dish.dishName} - ${dish.get_price()}"

    productsMenu.description += f"\n\nShowing {totalDishesToDisplay} items out of {len(dishManager.dishes)}."
    productsMenu.description += f"\nPage {page + 1} / {maxPages}"

    if page > 0:
        productsMenu.add_option("Previous Page", lambda: display_dishes(dishManager, page - 1))

    if page < maxPages - 1:
        productsMenu.add_option("Next Page", lambda: display_dishes(dishManager, page + 1))

    productsMenu.process()

# Ingredients inventory
def display_inventory(inventoryManager: InventoryManager, page: int):
    maxPages = math.floor(len(inventoryManager.items) / 10)

    # The index to use for printing the orders array
    itemsStart = page * 10

    # Only list up to a max of 10 orders.
    totalItemsToDisplay = min(10, len(inventoryManager.items) - itemsStart)

    productsMenu = OptionMenu(f"Ingredient Inventory Control")
    productsMenu.automaticallyExit = True
    productsMenu.description = ""

    for i in range(itemsStart, itemsStart + totalItemsToDisplay):
        item = inventoryManager.items[i]
        productsMenu.description += f"\n  {i + 1}. {item.itemName} - ${item.amount}x"

    productsMenu.description += f"\n\nShowing {totalItemsToDisplay} items out of {len(inventoryManager.items)}."
    productsMenu.description += f"\nPage {page + 1} / {maxPages}"

    if page > 0:
        productsMenu.add_option("Previous Page", lambda: display_inventory(inventoryManager, page - 1))

    if page < maxPages - 1:
        productsMenu.add_option("Next Page", lambda: display_inventory(inventoryManager, page + 1))

    productsMenu.process()

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