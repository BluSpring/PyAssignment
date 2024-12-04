from util.accounts import Account
from util.dishes import DishManager
from util.pagination import create_pagination


# Product Browsing - Customer
class ProductBrowser:
    def __init__(self, products):
        self.products = products

    def browse_products(self):
        create_pagination(None, "Available Products", self.products, (lambda text: text), None, 0)

def init(account: Account):
    dishManager = DishManager()
    products = []

    for dish in dishManager.dishes:
        text = f"{dish.dishName} - ${dish.get_price()}"

        if dish.currentDiscount > 0:
            text += f" ({dish.currentDiscount * 100}% off, was ${dish.price})"

        if not dishManager.is_dish_available(dish):
            text = f"(unavailable) {text}"

        products.append(text)

    productBrowser = ProductBrowser(products)
    productBrowser.browse_products()