from util.accounts import Account

def init(account: Account):
    pass

discounts = {}

def add_discount(item_name, discount_percentage):
    discounts[item_name] = discount_percentage
    print(f"Discount added for {item_name}: {discount_percentage}%")

def remove_discount(item_name):
    if item_name in discounts:
        del discounts[item_name]
        print(f"Discount removed for {item_name}")
    else:
        print("Discount not found.")

def view_discounts():
    print("\n--- Current Discounts ---")
    for item, discount in discounts.items():
        print(f"{item}: {discount}%")
