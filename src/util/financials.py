import json
from datetime import datetime

from util.pagination import Manager


# Gets the current month.
def get_month() -> int:
    return datetime.now().month

# Gets the name of the current month.
def get_formatted_month(month: int) -> str:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    return months[month - 1]

# Gets the current month number from the name.
def get_month_from_formatted(monthName: str) -> int:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    for month in range(len(months)):
        if monthName.lower().strip() == months[month].lower():
            return month

    raise Exception(f"Invalid month name {monthName}!")

# Gets the current year.
def get_year() -> int:
    return datetime.now().year

# Formats the month and year into MM-YYYY.
def get_formatted_key(month: int, year: int) -> str:
    return f"{month:02d}-{year}"

class Finances:
    def __init__(self, revenue: float, expenses: float):
        self.revenue = revenue
        self.expenses = expenses

class FinanceEncoder(json.JSONEncoder):
    def default(self, o: Finances):
        return o.__dict__

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
            json.dump(self.finances, file, indent = 4, cls = FinanceEncoder)

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

        if not key in self.finances:
            raise Exception(f"Financial records for {get_formatted_month(month)} {year} do not exist!")

        return self.finances[key]

    # Gets the financial information for the current month.
    def get_current_finances(self) -> Finances:
        key = get_formatted_key(get_month(), get_year())

        if not key in self.finances:
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
        finances = self.finances[get_formatted_key(month, year)]

        if finances is None:
            raise Exception(f"No financial information for {get_formatted_month(month)} {year}.")

        net_income = finances.revenue - finances.expenses
        print(f"Financial Report for {get_formatted_month(month)} {year} - Revenue: ${finances.revenue}, Expenses: ${finances.expenses}, Net Income: ${net_income}")