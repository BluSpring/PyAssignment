import json
import time

from util.accounts import Account
from util.id_manager import IdManager
from util.utils import get_current_time_millis

class Order:
    username: str # Username of the account that placed the order
    orderId: int # Order ID, used internally.
    orderTime: int # Time the order was placed, in milliseconds
    items: list[str] # Stores a list of dish IDs
    status: str # The current order status.

    def __init__(self, username: str, orderId: int, orderTime: int):
        self.username = username
        self.orderId = orderId
        self.orderTime = orderTime
        self.items = []
        self.status = "pending"

# Order Status Types:
#   - pending - Used if an order hasn't been acknowledged by the chefs yet.
#   - preparing - Used when an order is being prepared by the chefs.
#   - delivering - Used when the order is being delivered.
#   - cancelled - Used if the order has been cancelled by either the restaurant or the customer.
#   - completed - Used if the order has completed delivery.

def validate_order_status(status: str) -> bool:
    return (status == "pending" or status == "preparing" or status == "delivering"
            or status == "cancelled" or status == "completed")

class OrderEncoder(json.JSONEncoder):
    def default(self, o: Order):
        return o.__dict__

def decode_order(obj: dict) -> Order:
    order = Order(obj["username"], obj["orderId"], obj["orderTime"])
    order.status = obj["status"]

    if not validate_order_status(order.status):
        raise RuntimeError(f"Order ID {order.orderId} has an invalid status: {order.status}")

    return order

class OrderManager:
    idManager: IdManager
    orders: list[Order]
    currentId: int

    def __init__(self):
        self.idManager = IdManager()
        self.orders = []
        self.currentId = 0
        self.load()

    def save(self):
        with open("orders.json", "w") as file:
            json.dump(self.orders, file, indent = 4, cls = OrderEncoder)

    def load(self):
        try:
            with open("orders.json", "r") as file:
                data = json.load(file, object_hook = decode_order)
                self.orders = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def get_order(self, orderId: int) -> Order | None:
        for order in self.orders:
            if order.orderId == orderId:
                return order

        return None

    def get_all_orders(self, account: Account) -> list[Order]:
        orders = []

        for order in self.orders:
            if order.username == account.username:
                orders.append(order)

        return orders

    # This should be used to create new orders, but not place them just yet.
    def create_new_order(self, account: Account) -> Order:
        return Order(account.username, self.idManager.get_and_increment_id("orders"), get_current_time_millis())

    # This should be used to place orders.
    def place_order(self, order: Order):
        if self.get_order(order.orderId) is not None:
            raise RuntimeError(f"This order has already been placed!")

        self.orders.append(order)
        self.save()