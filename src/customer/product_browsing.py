from util.accounts import Account

# Product Browsing - Customer
class ProductBrowser:
    def _init_(self, products):
        self.products = products

    def browse_products(self):
        print("Available Products:")
        for product in self.products:
            print(f"- {product}")

def init(account: Account):
    pass