from util.accounts import Account

# Transaction Completion - Cashier
class Transaction:
    def _init_(self):
        self.transactions = []

    def complete_transaction(self, transaction_details):
        self.transactions.append(transaction_details)
        print(f"Transaction completed: {transaction_details}")

def init(account: Account):
    pass