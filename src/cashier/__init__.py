import cashier.reporting
import cashier.manage_discount
import cashier.product_display
import cashier.transaction_completion
from util.accounts import AccountManager
from util.menu import OptionMenu

def init():
    accounts = AccountManager()
    account = accounts.create_login_menu("cashier")

    menu = OptionMenu("Cashier System")
    menu.add_option("Product Display", lambda: product_display.init(account))
    menu.add_option("Manage Discount", lambda: manage_discount.init(account))
    menu.add_option("Transaction Completion", lambda: transaction_completion.init(account))
    menu.add_option("Reporting", lambda: reporting.init(account))

    menu.process()