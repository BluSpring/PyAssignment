from util.accounts import Account

def init(account: Account):
    pass

inventory = {"Ingredient 1": 10, "Ingredient 2": 20, "Ingredient 3": 30}

def view_inventory():
    print("\n--- Inventory ---")
    for item, quantity in inventory.items():
        print(f"{item}: {quantity} units")

def update_inventory(item_name, quantity):
    if item_name in inventory:
        inventory[item_name] += quantity
        print(f"Updated {item_name}. New quantity: {inventory[item_name]}")
    else:
        print(f"{item_name} not found in inventory.")
