import hashlib
import json
import getpass

class Account:
    accountType: str = ""
    username: str = ""
    passwordHash: str = ""
    name: str = ""
    address: str = ""

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

class AccountManager:
    accounts: list[Account] = []

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
        for account in self.accounts:
            # Find account that matches the type and username
            if account.accountType == accountType and account.username == username:
                return account

        # Otherwise, return None if no accounts could be found.
        return None

    def create_account(self, accountType: str, username: str, password: str) -> Account:
        # Check if any accounts with the type and username already exist.
        if self.get_account(accountType, username) is not None:
            raise Exception(f"Account with username {username} already exists!")

        # Validate usernames and passwords
        if " " in username or "\n" in username:
            raise Exception("Invalid username! Username must not contain spaces or line breaks!")

        if len(password) < 8:
            raise Exception("Password must be longer than 8 characters!")

        # Hash the password as SHA256, for security.
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        account = Account(accountType, username, hashedPassword)

        # Add account to the accounts list.
        self.accounts.append(account)
        self.save()

        return account

    def create_register_menu(self, accountType: str) -> Account:
        username = input("Insert a username: ")
        password = getpass.getpass("Password: ")

        account = self.create_account(accountType, username, password)
        print()
        print(f"Successfully created account with username {username}!")
        return account

    def create_login_menu(self, accountType: str) -> Account:
        print(f"Logging in as {accountType}.")
        username = input("Username: ")
        account = self.get_account(accountType, username)

        if account is None:
            raise Exception("No account exists by that username!")

        password = getpass.getpass("Password: ")

        if hashlib.sha256(password.encode()).hexdigest() != account.passwordHash:
            raise Exception("Invalid password!")

        print()
        print(f"Successfully logged in as {username}.")

        return account