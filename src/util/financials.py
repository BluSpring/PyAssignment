# Financial Management - Manager
class FinancialManager:
    def _init_(self):
        self.revenue = 0
        self.expenses = 0

    def add_revenue(self, amount):
        self.revenue += amount
        print(f"Added revenue: ${amount}. Total revenue: ${self.revenue}")

    def add_expense(self, amount):
        self.expenses += amount
        print(f"Added expense: ${amount}. Total expenses: ${self.expenses}")

    def generate_report(self):
        net_income = self.revenue - self.expenses
        print(f"Financial Report - Revenue: ${self.revenue}, Expenses: ${self.expenses}, Net Income: ${net_income}")