import manager.customer_feedback
import manager.financial_management
import manager.inventory_control
import manager.order_management
import manager.system_administration
from util.accounts import AccountManager
from util.menu import OptionMenu

def init():
    accounts = AccountManager()

    # Create an automatic, permanent "root" admin account for managers to use primarily when the system is first being set up.
    if accounts.get_account("manager", "admin") is None:
        account = accounts.create_account("manager", "admin", "admin123")
        print("An admin account has been created automatically, as no admin account currently exists in the system.")
        print("Username: admin")
        print("Password: admin123")
        print("Please change the password of this admin account as soon as possible!")

        print()
        print(f"Successfully logged in as admin.")
    else:
        # Create a login menu for managers to use.
        account = accounts.create_login_menu("manager")

    # Create a menu for the managers to interact with, each pointing to different
    # tasks they can do.
    menu = OptionMenu("Manager System")
    menu.add_option("System Administration", lambda: system_administration.init(account))
    menu.add_option("Order Management", lambda: order_management.init(account))
    menu.add_option("Financial Management", lambda: financial_management.init(account))
    menu.add_option("Inventory Control", lambda: inventory_control.init(account))
    menu.add_option("Customer Feedback", lambda: customer_feedback.init(account))

    menu.process()