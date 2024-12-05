import json

from util.pagination import Manager, ManagerSerializer
from util.utils import *


class Finances:
    def __init__(self, revenue: float, expenses: float):
        self.revenue = revenue
        self.expenses = expenses

def decode_finances(obj: dict) -> Finances:
    return Finances(obj["revenue"], obj["expenses"])

# Financial Management - Manager
class FinancialManager(Manager[Finances]):
    finances: dict[str, Finances]

    def __init__(self):
        self.finances = {}
        self.load()

    def save(self):
        with open("finances.json", "w") as file:
            json.dump(self.finances, file, indent = 4, cls = ManagerSerializer)

    def load(self):
        try:
            with open("finances.json", "r") as file:
                data = json.load(file, object_hook = decode_finances)
                self.finances = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    # Gets the financial records for a specific month and year.
    def get_finances(self, month: int, year: int) -> Finances:
        key = get_formatted_key(month, year)

        if key not in self.finances:
            raise Exception(f"Financial records for {get_formatted_month(month)} {year} do not exist!")

        return self.finances[key]

    # Gets the financial information for the current month.
    def get_current_finances(self) -> Finances:
        key = get_formatted_key(get_month(), get_year())

        if key not in self.finances:
            self.finances[key] = Finances(0, 0)

        return self.finances[key]

    # Adds revenue to the current month.
    def add_revenue(self, amount):
        finances = self.get_current_finances()
        finances.revenue += amount
        self.save()
        print(f"Added revenue: ${amount}. Total revenue: ${finances.revenue}")

    # Adds expenses to the current month.
    def add_expense(self, amount):
        finances = self.get_current_finances()
        finances.expenses += amount
        self.save()
        print(f"Added expense: ${amount}. Total expenses: ${finances.expenses}")

    # Generates a report for a specific month and year.
    def generate_report(self, month: int, year: int):
        key = get_formatted_key(month, year)

        if key not in self.finances:
            raise Exception(f"No financial information for {get_formatted_month(month)} {year}.")

        finances = self.finances[key]

        if finances is None:
            raise Exception(f"No financial information for {get_formatted_month(month)} {year}.")

        net_income = finances.revenue - finances.expenses
        print(f"Financial Report for {get_formatted_month(month)} {year} - Revenue: ${finances.revenue}, Expenses: ${finances.expenses}, Net Income: ${net_income}")