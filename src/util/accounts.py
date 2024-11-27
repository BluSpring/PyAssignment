import getpass
import hashlib
import json


class Account:
    accountType: str
    username: str
    passwordHash: str
    name: str
    address: str

    def __init__(self, accountType: str, username: str, passwordHash: str):
        self.accountType = accountType
        self.username = username
        self.passwordHash = passwordHash
        self.name = ""
        self.address = ""

# Run serialization of the Account class
class AccountEncoder(json.JSONEncoder):
    def default(self, o: Account):
        return o.__dict__

def decode_account(obj: dict) -> Account:
    account = Account(obj["accountType"], obj["username"], obj["passwordHash"])
    account.name = obj["name"]
    account.address = obj["address"]

    return account

# Make sure the account type is valid.
def validate_account_type(accountType: str):
    if accountType != "manager" and accountType != "customer" and accountType != "chef" and accountType != "cashier":
        raise RuntimeError(f"Invalid account type {accountType}!")

def validate_password(password: str):
    password = password.strip()

    if len(password) < 8:
        raise Exception("Password must be longer than 8 characters!")

    if " " in password or "\n" in password:
        raise Exception("Invalid password! Password must not contain spaces or line breaks!")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class AccountManager:
    accounts: list[Account]

    def __init__(self):
        self.accounts = []
        self.load()

    def save(self):
        with open("accounts.json", "w") as file:
            json.dump(self.accounts, file, indent = 4, cls = AccountEncoder)

    def load(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file, object_hook = decode_account)
                self.accounts = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def get_account(self, accountType: str, username: str) -> Account | None:
        validate_account_type(accountType)

        for account in self.get_accounts_of_type(accountType):
            # Find account that matches the username
            if account.username == username:
                return account

        # Otherwise, return None if no accounts could be found.
        return None

    # Get all accounts that match the account type.
    def get_accounts_of_type(self, accountType: str) -> list[Account]:
        validate_account_type(accountType)
        accounts = []

        for account in self.accounts:
            if account.accountType == accountType:
                accounts.append(account)

        return accounts

    def create_account(self, accountType: str, username: str, password: str) -> Account:
        validate_account_type(accountType)

        # Check if any accounts with the type and username already exist.
        if self.get_account(accountType, username) is not None:
            raise Exception(f"Account with username {username} already exists!")

        # Validate usernames and passwords
        if " " in username or "\n" in username:
            raise Exception("Invalid username! Username must not contain spaces or line breaks!")

        validate_password(password)

        # Hash the password as SHA256, for security.
        hashedPassword = hash_password(password)
        account = Account(accountType, username, hashedPassword)

        # Add account to the accounts list.
        self.accounts.append(account)
        self.save()

        return account

    def create_register_menu(self, accountType: str) -> Account:
        validate_account_type(accountType)

        username = input("Insert a username: ")
        password = getpass.getpass("Insert a password: ")
        verify_password = getpass.getpass("Confirm your password: ")

        if verify_password != password:
            raise Exception("Password and confirm password fields did not match!")

        account = self.create_account(accountType, username, password)
        print()
        print(f"Successfully created account with username {username}!")
        return account

    def create_login_menu(self, accountType: str) -> Account:
        validate_account_type(accountType)

        print(f"Logging in as {accountType}.")
        username = input("Username: ")
        account = self.get_account(accountType, username)

        if account is None:
            raise Exception("No account exists by that username!")

        password = getpass.getpass("Password: ")

        if hash_password(password) != account.passwordHash:
            raise Exception("Invalid password!")

        print()
        print(f"Successfully logged in as {username}.")

        return account