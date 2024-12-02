from util.accounts import Account


def init(account: Account):
    pass

class Order:
    def __init__(self, order_id, customer_name, items, total_price, status="Pending"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items
        self.total_price = total_price
        self.status = status

    def update_status(self, new_status):
        self.status = new_status


        return f"Order ID: {self.order_id}, Customer: {self.customer_name}, Status: {self.status}, Total: ${self.total_price}"

orders = []

def create_order(order_id, customer_name, items):
    total_price = sum([q * p for _, q, p in items])
    new_order = Order(order_id, customer_name, items, total_price)


def update_order_status(order_id, new_status):
    for order in orders:
        if order.order_id == order_id:
            order.update_status(new_status)

    print("Order not found.")

def display_orders():

    for order in orders:
        print(order)
