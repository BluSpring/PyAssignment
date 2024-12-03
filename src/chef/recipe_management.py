from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu
from util.pagination import create_pagination

def add_additional_options(menu: OptionMenu, dishManager: DishManager):
    menu.add_option("View Recipe", lambda: view_recipe(dishManager))
    menu.add_option("Add Recipe Instruction", lambda: add_recipe(dishManager))
    menu.add_option("Edit Recipe Instruction", lambda: edit_recipe(dishManager))
    menu.add_option("Remove Recipe Instruction", lambda: remove_recipe(dishManager))

def init(account: Account):
    dishManager = DishManager()
    create_pagination(dishManager, "Recipe Management", dishManager.dishes, (lambda dish: f"{dish.dishName} - {len(dish.recipe)} steps"), lambda menu: add_additional_options(menu, dishManager), 0)

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