from manager.order_management import Order
from util.accounts import Account, AccountManager
from util.dishes import DishManager
from util.orders import OrderManager


# Transaction Completion - Cashier
def complete_transaction(order: Order):
    dishManager = DishManager()
    accountManager = AccountManager()
    account = accountManager.get_account("customer", order.username)

    print(f"Receipt for Order #{order.orderId}")
    print(f"  Customer Name: {account.name}")

    for item in order.items:
        dish = dishManager.get_dish_lenient(item)
        print(f"  - {dish.dishName}: ${dish.get_price()}")

def init(account: Account):
    orderManager = OrderManager()
    orderId = int(input("Insert an order ID: "))
    order = orderManager.get_order(orderId)

    if order is None:
        raise Exception(f"Order does not exist!")

    complete_transaction(order)

    pass