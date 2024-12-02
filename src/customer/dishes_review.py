import json

from util.accounts import Account
from util.dishes import DishManager
from util.menu import OptionMenu


# Dishes Review - Customer
class DishReview:
    reviews: dict[str, list[str]] # Dish Name - List of Reviews

    def _init_(self):
        self.reviews = {}
        self.load()

    def save(self):
        with open("reviews.json", "w") as file:
            json.dump(self.reviews, file, indent = 4)

    def load(self):
        try:
            with open("reviews.json", "r") as file:
                data = json.load(file)
                self.reviews = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def add_review(self, dish, review):
        if dish not in self.reviews:
            self.reviews[dish] = []
        self.reviews[dish].append(review)
        self.save()
        print(f"Review added for {dish}: {review}")

    def view_reviews(self, dish):
        if dish in self.reviews:
            print(f"Reviews for {dish}:")
            for review in self.reviews[dish]:
                print(f"- {review}")
        else:
            print(f"No reviews available for {dish}")

def add_review(dishManager: DishManager, dishReview: DishReview):
    dishName = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception(f"Could not find dish with name \"{dishName}\"!")

    review = input("Insert a review for the dish: ")
    dishReview.add_review(dish, review)

def view_reviews(dishManager: DishManager, dishReview: DishReview):
    dishName = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception(f"Could not find dish with name \"{dishName}\"!")

    dishReview.view_reviews(dish.dishName)

def init(account: Account):
    dishManager = DishManager()
    dishReview = DishReview()

    reviewMenu = OptionMenu("Dishes Review")
    reviewMenu.description = "You can browse reviews of dishes here. Additionally, you may add your own reviews about the dishes here."

    reviewMenu.add_option("Add Review", lambda: add_review(dishManager, dishReview))
    reviewMenu.add_option("View Reviews", lambda: view_reviews(dishManager, dishReview))

    reviewMenu.process()