from util.accounts import Account

# Reporting - Cashier
class Reporting:
    def _init_(self):
        self.sales = []

    def record_sale(self, sale):
        self.sales.append(sale)
        print(f"Sale recorded: {sale}")

    def generate_sales_report(self):
        print("Sales Report:")
        for sale in self.sales:
            print(f"- {sale}")

def init(account: Account):
    pass