import getpass

from util.accounts import Account, AccountManager, hash_password, validate_password
from util.menu import OptionMenu


def change_name(accountManager: AccountManager, account: Account):
    newName = input("Insert a new name: ").strip()

    if len(newName) <= 0:
        raise Exception(f"Name must not be empty!")

    oldName = account.name
    account.name = newName
    accountManager.save()

    print("Successfully changed name.")
    print(f"Old: {oldName}")
    print(f"New: {newName}")

def change_password(accountManager: AccountManager, account: Account):
    oldPassword = getpass.getpass("Insert your old password: ")

    if hash_password(oldPassword) != account.passwordHash:
        raise Exception("Password does not match your old password!")

    newPassword = getpass.getpass("Insert your new password: ")
    validate_password(newPassword)

    verifyPassword = getpass.getpass("Verify new password: ")

    if newPassword != verifyPassword:
        raise Exception("Password and confirm password fields did not match!")

    account.passwordHash = hash_password(newPassword)
    accountManager.save()

    print("Successfully changed password.")

def change_address(accountManager: AccountManager, account: Account):
    newAddress = input("Insert a new address: ").strip()

    if len(newAddress) <= 0:
        raise Exception(f"Address must not be empty!")

    oldAddress = account.address
    account.address = newAddress
    accountManager.save()

    print("Successfully changed address.")
    print(f"Old: {oldAddress}")
    print(f"New: {newAddress}")

def init(accountManager: AccountManager, account: Account):
    menu = OptionMenu("Account Manager")
    menu.description = "You can manage your own account's personal information here."
    menu.description += f"\nUsername: {account.username}"
    menu.description += f"\nName: {account.name if account.name != '' else '(none)'}"
    menu.description += f"\nAddress: {account.address if account.address != '' else '(none)'}"

    menu.add_option("Change Name", lambda: change_name(accountManager, account))
    menu.add_option("Change Password", lambda: change_password(accountManager, account))
    menu.add_option("Change Address", lambda: change_address(accountManager, account))
    menu.process()