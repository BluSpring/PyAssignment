from util.accounts import Account

# Dishes Review - Customer
class DishReview:
    def _init_(self):
        self.reviews = {}

    def add_review(self, dish, review):
        if dish not in self.reviews:
            self.reviews[dish] = []
        self.reviews[dish].append(review)
        print(f"Review added for {dish}: {review}")

    def view_reviews(self, dish):
        if dish in self.reviews:
            print(f"Reviews for {dish}:")
            for review in self.reviews[dish]:
                print(f"- {review}")
        else:
            print(f"No reviews available for {dish}")

def init(account: Account):
    pass