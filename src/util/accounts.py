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

class AccountManager:
    accounts: list[Account] = []

    def __init__(self):
        self.load()

    def save(self):
        with open("accounts.json", "w") as file:
            json.dump(self.accounts, file, indent = 4)

    def load(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                self.accounts = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def get_account(self, accountType: str, username: str) -> Account | None:
        for account in self.accounts:
            # Find account that matches the type and username
            if account.accountType == accountType and account.username == account.username:
                return account

        # Otherwise, return None if no accounts could be found.
        return None

    def create_account(self, accountType: str, username: str, password: str) -> Account:
        # Check if any accounts with the type and username already exist.
        if self.get_account(accountType, username) is not None:
            raise Exception(f"Account with username {username} already exists!")

        # Hash the password as SHA256, for security.
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        account = Account(accountType, username, hashedPassword)

        # Add account to the accounts list.
        self.accounts.append(account)
        self.save()

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