from util.accounts import Account
from util.dishes import DishManager


# Product Browsing - Customer
class ProductBrowser:
    def __init__(self, products):
        self.products = products

    def browse_products(self):
        print("Available Products:")
        for product in self.products:
            print(f"- {product}")

def init(account: Account):
    dishManager = DishManager()
    products = []

    for dish in dishManager.dishes:
        products.append(f"{dish.dishName} - ${dish.price}")

    productBrowser = ProductBrowser(products)
    productBrowser.browse_products()