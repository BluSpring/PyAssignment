from util.accounts import Account
from util.menu import OptionMenu
from util.orders import OrderManager, Order
from util.pagination import create_pagination
from util.utils import millis_to_formatted_date_time, proper_case


def init(account: Account):
    orderManager = OrderManager()
    menu = OptionMenu("Order Management")

    menu.add_option("View Orders", lambda: display_orders(orderManager))
    menu.add_option("Update Order Status", lambda: handle_status_update(orderManager))

    menu.process()

def handle_status_update(orderManager: OrderManager):
    orderId = int(input("Insert an order ID: "))
    order = orderManager.get_order(orderId)

    if order is None:
        raise Exception("Order not found!")

    statusMenu = OptionMenu("Select Status")
    statusMenu.automaticallyExit = True
    statusMenu.description = f"Order #{order.orderId}"
    statusMenu.description += f"\nPlaced at {millis_to_formatted_date_time(order.orderTime)}"
    statusMenu.description += f"\nStatus: {order.status}"

    for status in ["pending", "preparing", "delivering", "cancelled", "completed"]:
        statusMenu.add_option(proper_case(status), lambda: update_order_status(orderManager, order, status))

    statusMenu.process()

def update_order_status(orderManager: OrderManager, order: Order, status: str):
    order.status = status
    orderManager.save()
    print(f"Successfully set order status to {proper_case(status)}.")

def display_orders(orderManager: OrderManager):
    orders: list[Order] = list(orderManager.orders)
    orders.sort(key = lambda x: x.orderTime, reverse = True)

    create_pagination(orderManager, "All Orders", orders, (lambda order: f"Order #{order.orderId} ({millis_to_formatted_date_time(order.orderTime)}) - {proper_case(order.status)}"), None, 0)
