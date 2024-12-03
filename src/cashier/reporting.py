from datetime import datetime

from util.accounts import Account
from util.dishes import DishManager
from util.financials import get_month_from_formatted, FinancialManager, get_formatted_month, get_month, get_year
from util.orders import OrderManager
from util.pagination import create_pagination


# Reporting - Cashier

def init(account: Account):
    financeManager = FinancialManager()
    orderManager = OrderManager()
    dishManager = DishManager()

    print("--- Sales Reporting ---")
    print(f"Currently Tracking: {get_formatted_month(get_month())} {get_year()}")

    year = int(input("Insert a year: "))
    monthTxt = input("Insert a month (i.e. March, 03): ")

    if monthTxt.isnumeric():
        month = int(monthTxt)
    else:
        month = get_month_from_formatted(monthTxt)

    finances = financeManager.get_finances(month, year)

    # Dish name to amount ordered
    items: dict[str, int] = {}

    for order in orderManager.orders:
        date = datetime.fromtimestamp(order.orderTime / 1000)

        if date.month != month or date.year != year:
            continue

        for item in order.items:
            dish = dishManager.get_dish_lenient(item)
            if not dish.dishName in items:
                items[dish.dishName] = 0

            items[dish.dishName] = items[dish.dishName] + 1

    itemKeys: list[str] = list(items.keys())
    itemKeys.sort(key = lambda x: items[x], reverse = True)

    print(f"Sales Report for {get_formatted_month(month)} {year}:")
    print(f"  Total Revenue: ${finances.revenue}")
    print(f"  Total Expenses: ${finances.expenses}")
    print(f"  Net Income: ${finances.revenue - finances.expenses}")

    if len(itemKeys) > 0:
        create_pagination(None, "Popular Dishes:", itemKeys, (lambda x: f"{x} - {items[x]} sold"), None, 0)
    else:
        print(f"No dishes were sold.")