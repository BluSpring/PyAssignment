import getpass

from util.accounts import Account, AccountManager, validate_password, hash_password
from util.menu import OptionMenu
from util.pagination import create_pagination
from util.utils import proper_case


def add_additional_options(accountMenu: OptionMenu, accountManager: AccountManager, accountType: str, accounts: list[Account]):
    accountMenu.add_option("View Account Information", lambda: view_account(accounts))
    accountMenu.add_option("Change Password", lambda: change_account_password(accountManager, accounts))
    accountMenu.add_option("Create New Account", lambda: create_account(accountManager, accountType))
    accountMenu.add_option("Delete Account", lambda: delete_account(accountManager, accounts))

def create_account(accountManager: AccountManager, accountType: str):
    username = input("Insert a username: ")
    password = getpass.getpass("Insert a new password: ")
    validate_password(password)

    verify_password = getpass.getpass("Confirm new password: ")

    if verify_password != password:
        raise Exception("Password and confirm password fields did not match!")

    account = accountManager.create_account(accountType, username, password)
    accountManager.save()

    print(f"Created new {accountType} account with username {account.username}.")

def handle_type(accountManager: AccountManager, accountType: str):
    accounts = accountManager.get_accounts_of_type(accountType)

    create_pagination(accountManager, f"Accounts ({proper_case(accountType)})", accounts, (lambda account: f"{account.username} - {proper_case(account.name) if len(account.name) > 0 else '(no name provided)'}"), (lambda menu: add_additional_options(menu, accountManager, accountType, accounts)), 0)

def view_account(accounts: list[Account]):
    index = int(input("Insert the account ID you want to view (e.g. 1, 43, 73): ")) - 1
    account = accounts[index]

    print(f"Username: {account.username}")
    print(f"Account Type: {proper_case(account.accountType)}")
    print(f"Name: {account.name}")
    print(f"Address: {account.address}")

def change_account_password(accountManager: AccountManager, accounts: list[Account]):
    index = int(input("Insert the account ID you want to modify: ")) - 1
    account = accounts[index]

    print(f"Changing password for username {account.username}.")

    password = getpass.getpass("Insert a new password: ")
    validate_password(password)

    verify_password = getpass.getpass("Confirm new password: ")

    if verify_password != password:
        raise Exception("Password and confirm password fields did not match!")

    # Hash the password as SHA256, for security.
    hashedPassword = hash_password(password)

    account.passwordHash = hashedPassword
    accountManager.save()
    print(f"Changed the password for username {account.username}!")

def delete_account(accountManager: AccountManager, accounts: list[Account]):
    index = int(input("Insert the account ID you want to delete: ")) - 1
    account = accounts[index]

    if account.username == "admin" and account.accountType == "manager":
        raise Exception("You're not allowed to delete the admin account!")

    accountManager.accounts.remove(account)
    print(f"Deleted account with username {account.username}.")

def init(account: Account):
    accountManager = AccountManager()

    selectTypeMenu = OptionMenu("Select Account Type")
    selectTypeMenu.description = "To proceed with managing accounts, please select an account type you want to manage."

    selectTypeMenu.add_option("Cashier", lambda: handle_type(accountManager, "cashier"))
    selectTypeMenu.add_option("Chef", lambda: handle_type(accountManager, "chef"))
    selectTypeMenu.add_option("Customer", lambda: handle_type(accountManager, "customer"))
    selectTypeMenu.add_option("Manager", lambda: handle_type(accountManager, "manager"))

    selectTypeMenu.process()

    pass