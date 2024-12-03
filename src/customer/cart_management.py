from util.accounts import Account, AccountManager
from util.dishes import DishManager, Dish
from util.menu import OptionMenu
from util.orders import OrderManager


def init(account: Account):
    accountManager = AccountManager()
    # Use updated account under this manager
    account = accountManager.get_account(account.accountType, account.username)

    menu = OptionMenu("Shopping Cart")
    update_menu_description(menu, account)

    menu.add_option("Add Dish to Cart", lambda: add_item(menu, accountManager, account))
    menu.add_option("Remove Dish from Cart", lambda: remove_item(menu, accountManager, account))
    menu.add_option("View Shopping Cart", lambda: view_cart(account))
    menu.add_option("Place Order", lambda: place_order(menu, accountManager, account))

    menu.process()

def update_menu_description(menu: OptionMenu, account: Account):
    menu.description = "In this menu, you can manage your shopping cart!"
    menu.description += f"\nYou currently have {len(account.cart)} item(s) in your cart."

def add_item(menu: OptionMenu, accountManager: AccountManager, account: Account):
    dishManager = DishManager()
    dishName = input("Insert a dish name: ")

    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception("No dish exists with that name!")

    quantity = int(input("Insert an amount to add: "))

    if quantity < 1:
        raise Exception("The amount must not be less than zero!")

    for i in range(quantity):
        account.cart.append(dish.dishName)

    print(f"Added {quantity}x {dish.dishName} to cart.")
    accountManager.save()
    update_menu_description(menu, account)

def remove_item(menu: OptionMenu, accountManager: AccountManager, account: Account):
    dishManager = DishManager()
    dishName = input("Insert a dish name: ")

    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception("No dish exists with that name!")

    quantity = int(input("Insert a quantity to remove: "))

    if quantity < 1:
        raise Exception("The amount must not be less than zero!")

    for i in range(quantity):
        account.cart.remove(dish.dishName)

    print(f"Removed {quantity}x {dish.dishName} from cart.")
    accountManager.save()
    update_menu_description(menu, account)

def view_cart(account: Account):
    dishManager = DishManager()
    print(f"Shopping Cart ({len(account.cart)} item(s)): ")

    totals: dict[Dish, int] = {}

    for dishName in account.cart:
        dish = dishManager.get_dish(dishName)

        if dish not in totals:
            totals[dish] = 0

        totals[dish] = totals[dish] + 1

    totalPrice = 0.0

    for dish, total in totals:
        price = dish.get_price() * total
        print(f"{dish.dishName}: {total} x ${price}")
        totalPrice += price

    print(f"Total: ${totalPrice}")

def place_order(menu: OptionMenu, accountManager: AccountManager, account: Account):
    orderManager = OrderManager()
    order = orderManager.create_new_order(account)
    order.items = list(account.cart)
    account.cart = []

    orderManager.place_order(order)
    accountManager.save()
    print(f"Successfully placed order #{order.orderId} with the {len(order.items)} item(s) in your shopping cart.")

    update_menu_description(menu, account)