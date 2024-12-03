from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu


def init(account: Account):
    discounts = {}

    dishManager = DishManager()
    for dish in dishManager.dishes:
        if dish.currentDiscount > 0:
            discounts[dish.dishName] = dish.currentDiscount * 100

    cachedDiscounts = discounts.copy()
    menu = OptionMenu("Manage Discounts")

    menu.add_option("Add Discount", lambda: handle_add_discount(dishManager, discounts, cachedDiscounts))
    menu.add_option("Remove Discount", lambda: handle_remove_discount(dishManager, discounts, cachedDiscounts))
    menu.add_option("View Discounts", lambda: view_discounts(discounts))

    menu.process()

def handle_add_discount(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    name = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(name)

    if dish is None:
        raise Exception("Failed to find a dish with that name!")

    percentage = float(input("Insert a new discount percentage: "))

    if percentage < 0 or percentage > 100:
        raise Exception("Discount percentage must be between 0% and 100%!")

    add_discount(discounts, dish.dishName, percentage)
    update_discounts(dishManager, discounts, cachedDiscounts)


def handle_remove_discount(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    name = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(name)

    if dish is None:
        raise Exception("Failed to find a dish with that name!")

    remove_discount(discounts, dish.dishName)
    update_discounts(dishManager, discounts, cachedDiscounts)

def update_discounts(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    # Search for added discounts
    discountAdded = False

    for itemName in discounts:
        if not itemName in cachedDiscounts or discounts[itemName] != cachedDiscounts[itemName]:
            percentage = discounts[itemName]
            dish = dishManager.get_dish(itemName)
            dish.currentDiscount = percentage / 100
            discountAdded = True

    # Search for removed discounts
    if not discountAdded:
        for itemName in cachedDiscounts:
            if not itemName in discounts:
                dish = dishManager.get_dish(itemName)
                dish.currentDiscount = 0

    dishManager.save()

def add_discount(discounts, itemName, discountPercentage):
    discounts[itemName] = discountPercentage
    print(f"Discount added for {itemName}: {discountPercentage}%")

def remove_discount(discounts, itemName):
    if itemName in discounts:
        del discounts[itemName]
        print(f"Discount removed for {itemName}")
    else:
        print("Discount not found.")

def view_discounts(discounts):
    print("\n--- Current Discounts ---")
    for item, discount in discounts.items():
        print(f"{item}: {discount}%")
