from util.accounts import Account
from util.dishes import DishManager, Dish
from util.pagination import create_pagination

def format_dish_display(dish: Dish) -> str:
    name = f"{dish.dishName} - ${dish.get_price()}"
    if dish.currentDiscount > 0:
        name += f" ({dish.currentDiscount * 100}% off, was ${dish.price})"

    return name

def init(account: Account):
    dishManager = DishManager()

    create_pagination(dishManager, "Product Display", dishManager.dishes, (lambda dish: format_dish_display(dish)), None, 0)