import math

from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu


def display_dishes(dishManager: DishManager, page: int):
    maxPages = math.floor(len(dishManager.dishes) / 10)

    # The index to use for printing the orders array
    itemsStart = page * 10

    # Only list up to a max of 10 orders.
    totalDishesToDisplay = min(10, len(dishManager.dishes) - itemsStart)

    productsMenu = OptionMenu(f"Recipe Management")
    productsMenu.automaticallyExit = True
    productsMenu.description = ""

    for i in range(itemsStart, itemsStart + totalDishesToDisplay):
        dish = dishManager.dishes[i]
        productsMenu.description += f"\n  {i + 1}. {dish.dishName} - {len(dish.recipe)} steps"

    productsMenu.description += f"\n\nShowing {totalDishesToDisplay} items out of {len(dishManager.dishes)}."
    productsMenu.description += f"\nPage {page + 1} / {maxPages}"

    productsMenu.add_option("View Recipe", lambda: view_recipe(dishManager))
    productsMenu.add_option("Add Recipe Instruction", lambda: add_recipe(dishManager))
    productsMenu.add_option("Edit Recipe Instruction", lambda: edit_recipe(dishManager))
    productsMenu.add_option("Remove Recipe Instruction", lambda: remove_recipe(dishManager))

    if page > 0:
        productsMenu.add_option("Previous Page", lambda: display_dishes(dishManager, page - 1))

    if page < maxPages - 1:
        productsMenu.add_option("Next Page", lambda: display_dishes(dishManager, page + 1))

    productsMenu.process()

def init(account: Account):
    dishManager = DishManager()

    display_dishes(dishManager, 0)

    pass

def view_recipe(dishManager: DishManager):
    index = int(input("Insert a dish number to view: ")) - 1
    dish = dishManager.dishes[index]

    print(f"Recipe for {dish.dishName}:")

    for i in range(len(dish.recipe)):
        print(f"{i + 1}. {dish.recipe[i]}")

def add_recipe(dishManager: DishManager):
    index = int(input("Insert a dish number to view: ")) - 1
    dish = dishManager.dishes[index]
    line = input("Insert an instruction: ")

    dish.recipe.append(line)
    dishManager.save()
    print(f"Added instruction to recipe for {dish.dishName}!")

def remove_recipe(dishManager: DishManager):
    index = int(input("Insert a dish number to view: ")) - 1
    dish = dishManager.dishes[index]
    line = int(input("Insert an instruction line to remove: ")) - 1
    recipeLine = dish.recipe[line]

    dish.recipe.remove(recipeLine)
    dishManager.save()

    print(f"Removed instruction \"{recipeLine}\" from recipe {dish.dishName}!")

def edit_recipe(dishManager: DishManager):
    index = int(input("Insert a dish number to view: ")) - 1
    dish = dishManager.dishes[index]
    line = int(input("Insert an instruction line to edit: ")) - 1
    newLine = input("Insert a new instruction: ")

    recipeLine = dish.recipe[line]
    dish.recipe[line] = newLine
    dishManager.save()

    print(f"Replaced instruction \"{recipeLine}\" for recipe {dish.dishName}!")