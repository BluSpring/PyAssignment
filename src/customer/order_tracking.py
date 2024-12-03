from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu
from util.orders import OrderManager, Order
from util.pagination import create_pagination
from util.utils import proper_case

def view_order(orders: list[Order]):
    dishManager = DishManager()
    orderId = int(input("Insert the order ID that you want to view: "))
    currentOrder: Order | None = None

    for order in orders:
        if order.orderId == orderId:
            currentOrder = order
            break

    if currentOrder is None:
        raise Exception("Invalid order ID!")

    print(f"Order ID: {currentOrder.orderId}")
    print(f"Status: {proper_case(currentOrder.status)}")
    print(f"Ordered Items: ({len(currentOrder.items)})")

    countedItems: dict[str, int] = {}

    # Total up any duplicate items.
    for item in currentOrder.items:
        if countedItems[item] is None:
            countedItems[item] = 0

        countedItems[item] = countedItems[item] + 1

    for item in countedItems.keys():
        total = countedItems[item]
        dish = dishManager.get_dish_lenient(item)
        print(f" - ({total}x) {dish.dishName} (${dish.price * total})")

def cancel_order(orderManager: OrderManager, orders: list[Order]):
    orderId = int(input("Insert the order ID that you want to cancel: "))
    currentOrder: Order | None = None

    for order in orders:
        if order.orderId == orderId:
            currentOrder = order
            break

    if currentOrder is None:
        raise Exception("Invalid order ID!")

    if currentOrder.status == "completed":
        raise Exception("You cannot cancel an already completed order!")

    if currentOrder.status == "delivering":
        raise Exception("You cannot cancel an order that is already being delivered!")

    currentOrder.status = "cancelled"
    orderManager.save()

def add_additional_options(menu: OptionMenu, orderManager: OrderManager, orders: list[Order]):
    menu.description = "In this menu, you can track the status of all of your orders, and cancel any unfulfilled orders."
    menu.description += "\n\nOrders:"

    menu.add_option("View Order", lambda: view_order(orders))
    menu.add_option("Cancel Order", lambda: cancel_order(orderManager, orders))

def init(account: Account):
    orderManager = OrderManager()
    # Get all orders for the account, sorted by the most recent orders.
    currentOrders = orderManager.get_all_orders(account)
    currentOrders.sort(key = lambda x: x.orderTime, reverse = True)

    create_pagination(orderManager, "Order Tracking", currentOrders, (lambda order: f"Order #{order.orderId} - {proper_case(order.status)}"), (lambda menu: add_additional_options(menu, orderManager, currentOrders)), 0)