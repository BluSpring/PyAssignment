from util.accounts import Account
from util.financials import FinancialManager, get_month, get_year, get_formatted_month, get_month_from_formatted
from util.menu import OptionMenu


def init(account: Account):
    financeManager = FinancialManager()
    menu = OptionMenu("Financial Management")
    menu.description = f"Tracking financials for {get_formatted_month(get_month())} {get_year()}."

    menu.add_option("Add Revenue", lambda: add_revenue(financeManager))
    menu.add_option("Add Expense", lambda: add_expense(financeManager))
    menu.add_option("Generate Report", lambda: generate_report(financeManager))

    menu.process()

def add_revenue(financeManager: FinancialManager):
    amount = float(input("Insert revenue to add: $").strip())
    financeManager.add_revenue(amount)
    financeManager.save()

def add_expense(financeManager: FinancialManager):
    amount = float(input("Insert expense to add: $").strip())
    financeManager.add_expense(amount)
    financeManager.save()

def generate_report(financeManager: FinancialManager):
    monthTxt = input("Insert a month (i.e. March, 03): ")

    if monthTxt.isnumeric():
        month = int(monthTxt)
    else:
        month = get_month_from_formatted(monthTxt)

    year = int(input("Insert a year: "))
    financeManager.generate_report(month, year)