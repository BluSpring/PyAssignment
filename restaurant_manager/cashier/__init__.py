from ..util.accounts import AccountManager

def init():
    accounts = AccountManager()
    account = accounts.create_menu("cashier")