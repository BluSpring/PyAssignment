from util.accounts import Account

def init(account: Account):
    pass








class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item_name, quantity, price):
        self.items.append((item_name, quantity, price))
        print(f"Added {quantity} x {item_name} to cart.")

    def remove_item(self, item_name):
        for item in self.items:
            if item[0] == item_name:
                self.items.remove(item)
                print(f"Removed {item_name} from cart.")
                return
        print("Item not found in cart.")

    def view_cart(self):
        print("\n Cart ")
        for item, quantity, price in self.items:
            print(f"{item}: {quantity} x ${price}")
        total = sum([q * p for _, q, p in self.items])
        print(f"Total: ${total}")


