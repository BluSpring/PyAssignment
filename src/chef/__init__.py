import chef.equipment_management
import chef.inventory_check
import chef.production_record_keeping
import chef.recipe_management
from util.accounts import AccountManager
from util.menu import OptionMenu


def init():
    # Create a login menu for the chefs to log into
    accounts = AccountManager()
    account = accounts.create_login_menu("chef")

    # Create a menu for the chefs to interact with, each pointing to different
    # tasks they can do.
    menu = OptionMenu("Chef System")
    menu.add_option("Recipe Management", lambda: recipe_management.init(account))
    menu.add_option("Inventory Check", lambda: inventory_check.init(account))
    menu.add_option("Production Record-keeping", lambda: production_record_keeping.init(account))
    menu.add_option("Equipment Management", lambda: equipment_management.init(account))

    menu.process()