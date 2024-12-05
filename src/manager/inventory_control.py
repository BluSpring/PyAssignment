from util.accounts import Account
from util.dishes import DishManager, Dish
from util.inventory import InventoryManager, InventoryItem
from util.menu import OptionMenu
from util.pagination import create_pagination

# Dishes inventory
def add_dish_options(menu: OptionMenu, dishManager: DishManager):
    menu.add_option("Add Dish", lambda: add_dish(dishManager))
    menu.add_option("Remove Dish", lambda: remove_dish(dishManager))
    menu.add_option("Add Item to Dish", lambda: add_item_to_dish(dishManager))

def add_dish(dishManager: DishManager):
    dishName = input("Insert a dish name: ")
    price = float(input("Insert a price: $"))

    if dishManager.get_dish_lenient(dishName) is not None:
        raise Exception("A dish with that name already exists!")

    dishManager.dishes.append(Dish(dishName, [], price, []))
    dishManager.save()
    print(f"Added new dish {dishName} with price ${price} to inventory.")

def add_item_to_dish(dishManager: DishManager):
    inventoryManager = InventoryManager()
    dishName = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception("A dish with that name does not exist!")

    itemName = input("Insert an item name: ")
    item = inventoryManager.get_item_lenient(itemName)

    if item is None:
        raise Exception("An item with that name does not exist!")

    dish.items.append(item.itemName)
    dishManager.save()

    print(f"Added item {item.itemName} to dish {dish.dishName}.")

def remove_dish(dishManager: DishManager):
    dishName = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception("A dish with that name does not exist!")

    dishManager.dishes.remove(dish)
    dishManager.save()

    print(f"Removed dish {dish.dishName} from inventory.")

def display_dishes(dishManager: DishManager, page: int):
    create_pagination(dishManager, "Dish Inventory Control", dishManager.dishes, (lambda dish: f"{dish.dishName} - ${dish.price}"), (lambda menu: add_dish_options(menu, dishManager)), page)

# Ingredients inventory
def add_inventory_options(menu: OptionMenu, inventoryManager: InventoryManager):
    menu.add_option("Add Ingredient", lambda: add_item(inventoryManager))
    menu.add_option("Remove Ingredient", lambda: remove_item(inventoryManager))
    menu.add_option("Update Ingredient Quantity", lambda: update_item(inventoryManager))

def add_item(inventoryManager: InventoryManager):
    itemName = input("Insert an item name: ")
    price = float(input("Insert a price: $"))
    item = InventoryItem(itemName, price, 0)

    if inventoryManager.get_item_lenient(itemName) is not None:
        raise Exception("An item with that name already exists!")

    inventoryManager.items.append(item)
    inventoryManager.save()
    print(f"Added new item {itemName} with price ${price} to inventory.")

def update_item(inventoryManager: InventoryManager):
    itemName = input("Insert an item name: ")
    item = inventoryManager.get_item_lenient(itemName)

    if item is None:
        raise Exception("An item with that name does not exist!")

    print()
    print(f"Current quantity: {item.amount} units")

    amount = int(input("Insert a new amount: "))

    item.amount = amount
    inventoryManager.save()

    print(f"Updated item {item.itemName} to {amount} units.")

def remove_item(inventoryManager: InventoryManager):
    itemName = input("Insert an item name: ")
    item = inventoryManager.get_item_lenient(itemName)

    if item is None:
        raise Exception("An item with that name does not exist!")

    inventoryManager.items.remove(item)
    inventoryManager.save()

    print(f"Removed item {item.itemName} from inventory.")

def display_inventory(inventoryManager: InventoryManager, page: int):
    create_pagination(inventoryManager, "Ingredient Inventory Control", inventoryManager.items, (lambda item: f"{item.itemName} - {item.amount} units (${item.price} / unit)"), (lambda menu: add_inventory_options(menu, inventoryManager)), page)

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