import math

from util.accounts import Account
from util.menu import OptionMenu
from util.orders import OrderManager, Order
from util.utils import proper_case

def display_orders(orderManager: OrderManager, orders: list[Order], page: int):
    maxPages = math.floor(len(orders) / 10)

    # The index to use for printing the orders array
    ordersStart = page * 10

    # Only list up to a max of 10 orders.
    totalOrdersToDisplay = min(10, len(orders) - ordersStart)

    orderMenu = OptionMenu("Tracked Orders")
    orderMenu.description = f"""
        In this menu, you can track the status of all of your orders, and cancel any unfulfilled orders.

        Orders:
        """

    for i in range(ordersStart, ordersStart + totalOrdersToDisplay):
        order = orders[i]
        orderMenu.description += f"\n  Order #{order.orderId} - {proper_case(order.status)}"

    orderMenu.description += f"\n\nShowing {totalOrdersToDisplay} items out of {len(orders)}."
    orderMenu.description += f"\nPage {page + 1} / {maxPages}"

    orderMenu.add_option("View Order", lambda: view_order(orders))
    orderMenu.add_option("Cancel Order", lambda: cancel_order(orderManager, orders))

    if page > 0:
        orderMenu.add_option("Previous Page", lambda: display_orders(orderManager, orders, page - 1))

    if page < maxPages - 1:
        orderMenu.add_option("Next Page", lambda: display_orders(orderManager, orders, page + 1))

    orderMenu.process()

def view_order(orders: list[Order]):
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
        # TODO: Use the actual dish name.
        print(f" - ({total}x) {item}")

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

def init(account: Account):
    orderManager = OrderManager()
    # Get all orders for the account, sorted by the most recent orders.
    currentOrders = orderManager.get_all_orders(account)
    currentOrders.sort(key = lambda x: x.orderTime, reverse = True)

    display_orders(orderManager, currentOrders, 0)