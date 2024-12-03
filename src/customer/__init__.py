import customer.account_management
import customer.cart_management
import customer.dishes_review
import customer.order_tracking
import customer.product_browsing
from util.accounts import AccountManager, Account
from util.menu import OptionMenu


# Python does not allow setting variables inside lambdas, so we have to work around it with this.
def create_login(accounts: AccountManager, accountWorkaround: dict):
    accountWorkaround["account"] = accounts.create_login_menu("customer")

def create_register(accounts: AccountManager, accountWorkaround: dict):
    accountWorkaround["account"] = accounts.create_register_menu("customer")

def init():
    accounts = AccountManager()

    # Python does not allow setting variables inside lambdas, so we have to work around it with this.
    accountWorkaround: dict = {"account": None}

    while accountWorkaround["account"] is None:
        try:
            menu = OptionMenu("Customer System")
            menu.description = """
Welcome, customer, to Amar's Restaurant!
Please log into your account, or create a new account, to be able to use our services.
            """
            menu.automaticallyExit = True

            menu.add_option("Log in to existing account", lambda: create_login(accounts, accountWorkaround))
            menu.add_option("Create new account", lambda: create_register(accounts, accountWorkaround))

            menu.process()

            if menu.exiting:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            print()

    account: Account = accountWorkaround["account"]

    if account is None:
        return

    menu = OptionMenu("Customer System")
    menu.description = """
Welcome, customer, to Amar's Restaurant!
Here, you can manage your account, go through our products, track your orders, and submit reviews about our dishes!
    """
    menu.add_option("Account Management", lambda: account_management.init(accounts, account))
    menu.add_option("Product Browsing", lambda: product_browsing.init(account))
    menu.add_option("Cart Management", lambda: cart_management.init(account))
    menu.add_option("Order Tracking", lambda: order_tracking.init(account))
    menu.add_option("Dishes Review", lambda: dishes_review.init(account))

    menu.process()
