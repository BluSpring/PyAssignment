from util.accounts import Account

def init(account: Account):
    pass

class ProductionRecord:
    def __init__(self, recipe_name, quantity, batch_number, date):
        self.recipe_name = recipe_name
        self.quantity = quantity
        self.batch_number = batch_number
        self.date = date

    def __str__(self):
        return f"Recipe: {self.recipe_name}, Quantity: {self.quantity}, Batch: {self.batch_number}, Date: {self.date}"

production_records = []

def log_production(recipe_name, quantity, batch_number, date):
    record = ProductionRecord(recipe_name, quantity, batch_number, date)
    production_records.append(record)
    print(f"Production logged: {record}")

def view_production_records():

    for record in production_records:
        print(record)
