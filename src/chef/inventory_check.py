from util.accounts import Account
from util.inventory import InventoryManager
from util.menu import OptionMenu
from util.pagination import create_pagination

def init(account: Account):
    inventoryManager = InventoryManager()

    menu = OptionMenu("Inventory Check")
    menu.add_option("View Inventory", lambda: view_inventory(inventoryManager))
    menu.add_option("Add to Inventory", lambda: handle_update_inventory(inventoryManager))
    menu.add_option("Remove from Inventory", lambda: handle_remove_inventory(inventoryManager))

def handle_update_inventory(inventoryManager: InventoryManager):
    itemName = input("Insert the item name: ")
    amount = int(input("Insert the added quantity: "))

    update_inventory(inventoryManager, itemName, amount)

def handle_remove_inventory(inventoryManager: InventoryManager):
    itemName = input("Insert the item name: ")
    amount = int(input("Insert the removed quantity: "))

    update_inventory(inventoryManager, itemName, -amount)

def view_inventory(inventoryManager: InventoryManager):
    create_pagination(inventoryManager, "Inventory", inventoryManager.items, (lambda inventoryItem: f"{inventoryItem.itemName}: {inventoryItem.amount} units"), None, 0)

def update_inventory(inventoryManager: InventoryManager, itemName, quantity):
    item = inventoryManager.get_item_lenient(itemName)

    if item is not None:
        # Ensure the quantity never goes below the item's actual quantity.
        if (item.amount + quantity) < 0:
            raise Exception(f"Quantity must not reduce below the item's quantity!")

        item.amount += quantity
        print(f"Updated {item.itemName}. New quantity: {item.amount}")
    else:
        raise Exception(f"{itemName} not found in inventory.")
