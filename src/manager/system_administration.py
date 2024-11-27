import getpass
import math

from util.accounts import Account, AccountManager, validate_password, hash_password
from util.menu import OptionMenu
from util.utils import proper_case


def display_accounts(accountManager: AccountManager, accountType: str, accounts: list[Account], page: int):
    maxPages = math.floor(len(accounts) / 10)

    # The index to use for printing the orders array
    accountsStart = page * 10

    # Only list up to a max of 10 orders.
    totalAccountsToDisplay = min(10, len(accounts) - accountsStart)

    accountMenu = OptionMenu("Accounts ({proper_case(accountType)})")
    accountMenu.description = ""

    for i in range(accountsStart, accountsStart + totalAccountsToDisplay):
        account = accounts[i]
        accountMenu.description += f"\n  {i + 1}. {account.username} - {proper_case(account.name)}"

    accountMenu.description += f"\n\nShowing {totalAccountsToDisplay} items out of {len(accounts)}."
    accountMenu.description += f"\nPage {page + 1} / {maxPages}"

    accountMenu.add_option("View Account Information", lambda: view_account(accounts))
    accountMenu.add_option("Change Password", lambda: change_account_password(accountManager, accounts))
    accountMenu.add_option("Delete Account", lambda: delete_account(accountManager, accounts))

    if page > 0:
        accountMenu.add_option("Previous Page", lambda: display_accounts(accountManager, accountType, accounts, page - 1))

    if page < maxPages - 1:
        accountMenu.add_option("Next Page", lambda: display_accounts(accountManager, accountType, accounts, page + 1))

    accountMenu.process()

def handle_type(accountManager: AccountManager, accountType: str):
    accounts = accountManager.get_accounts_of_type(accountType)
    display_accounts(accountManager, accountType, accounts, 0)

def view_account(accounts: list[Account]):
    index = int(input("Insert the account ID you want to view: ")) - 1
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

    accountManager.accounts.remove(account)
    print(f"Deleted account with username {account.username}.")

def init(account: Account):
    accountManager = AccountManager()

    selectTypeMenu = OptionMenu("Select Account Type")
    selectTypeMenu.description = """
    To proceed with managing accounts, please select an account type you want to manage.
    """

    selectTypeMenu.add_option("Cashier", lambda: handle_type(accountManager, "cashier"))
    selectTypeMenu.add_option("Chef", lambda: handle_type(accountManager, "chef"))
    selectTypeMenu.add_option("Customer", lambda: handle_type(accountManager, "customer"))
    selectTypeMenu.add_option("Manager", lambda: handle_type(accountManager, "manager"))

    selectTypeMenu.process()

    pass