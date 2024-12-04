from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu
from util.pagination import create_pagination


def init(account: Account):
    discounts = {}

    dishManager = DishManager()

    # The discount values are stored as values between 0 and 1, so convert them to proper percentage values.
    for dish in dishManager.dishes:
        if dish.currentDiscount > 0:
            discounts[dish.dishName] = dish.currentDiscount * 100

    cachedDiscounts = discounts.copy()
    menu = OptionMenu("Manage Discounts")

    menu.add_option("Add Discount", lambda: handle_add_discount(dishManager, discounts, cachedDiscounts))
    menu.add_option("Remove Discount", lambda: handle_remove_discount(dishManager, discounts, cachedDiscounts))
    menu.add_option("View Discounts", lambda: view_discounts(dishManager, discounts))

    menu.process()

def handle_add_discount(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    name = input("Insert a dish name: ")

    # Search for a dish with the provided name, with no case-sensitivity.
    dish = dishManager.get_dish_lenient(name)

    if dish is None:
        raise Exception("Failed to find a dish with that name!")

    percentage = float(input("Insert a new discount percentage: "))

    # Ensure the given percentage is valid
    if percentage < 0 or percentage > 100:
        raise Exception("Discount percentage must be between 0% and 100%!")

    add_discount(discounts, dish.dishName, percentage)
    update_discounts(dishManager, discounts, cachedDiscounts)


def handle_remove_discount(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    name = input("Insert a dish name: ")

    # Search for a dish with the provided name, with no case-sensitivity.
    dish = dishManager.get_dish_lenient(name)

    if dish is None:
        raise Exception("Failed to find a dish with that name!")

    remove_discount(discounts, dish.dishName)
    update_discounts(dishManager, discounts, cachedDiscounts)

def update_discounts(dishManager: DishManager, discounts: dict[str, float], cachedDiscounts: dict[str, float]):
    # Search for added discounts
    discountAdded = False

    # If the values between the previous discounts list and the current discounts list don't match,
    # find the ones that are either not included in the list or are not the same as the previous list.
    for itemName in discounts:
        if not itemName in cachedDiscounts or discounts[itemName] != cachedDiscounts[itemName]:
            # Update the current discounts list accordingly.
            percentage = discounts[itemName]
            dish = dishManager.get_dish(itemName)
            dish.currentDiscount = percentage / 100
            discountAdded = True

    # Search for removed discounts
    if not discountAdded:
        for itemName in cachedDiscounts:
            # If the dish does not exist in the current discounts list, then we can safely assume that it was
            # removed, and should set the discount to 0%.
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

def view_discounts(dishManager, discounts):
    print("\n--- Current Discounts ---")

    create_pagination(dishManager, "Current Discounts", discounts.keys(), (lambda name: f"{name}: {discounts[name]}%"), None, 0)
