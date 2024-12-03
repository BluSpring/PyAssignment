import math

from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu


def display_products(dishManager: DishManager, page: int):
    maxPages = math.floor(len(dishManager.dishes) / 10)

    # The index to use for printing the orders array
    itemsStart = page * 10

    # Only list up to a max of 10 orders.
    totalDishesToDisplay = min(10, len(dishManager.dishes) - itemsStart)

    productsMenu = OptionMenu(f"Product Display")
    productsMenu.automaticallyExit = True
    productsMenu.description = ""

    for i in range(itemsStart, itemsStart + totalDishesToDisplay):
        dish = dishManager.dishes[i]
        productsMenu.description += f"\n  {i + 1}. {dish.dishName} - ${dish.get_price()}"
        if dish.currentDiscount > 0:
            productsMenu.description += f" ({dish.currentDiscount * 100}% off, was ${dish.price})"

    productsMenu.description += f"\n\nShowing {totalDishesToDisplay} items out of {len(dishManager.dishes)}."
    productsMenu.description += f"\nPage {page + 1} / {maxPages}"

    if page > 0:
        productsMenu.add_option("Previous Page", lambda: display_products(dishManager, page - 1))

    if page < maxPages - 1:
        productsMenu.add_option("Next Page", lambda: display_products(dishManager, page + 1))

    productsMenu.process()

def init(account: Account):
    dishManager = DishManager()

    display_products(dishManager, 0)

    pass