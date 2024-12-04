import json

from util.accounts import Account
from util.menu import OptionMenu


# Customer Feedback - Manager
class CustomerFeedbackManager:
    feedbackList: list[str]

    def __init__(self):
        self.feedbackList = []
        self.load()

    def save(self):
        with open("customer_feedback.json", "w") as file:
            json.dump(self.feedbackList, file, indent = 4)

    def load(self):
        try:
            with open("customer_feedback.json", "r") as file:
                data = json.load(file)
                self.feedbackList = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def collect_feedback(self, feedback):
        self.feedbackList.append(feedback)
        self.save()
        print(f"Feedback collected: {feedback}")

    def view_feedback(self):
        print("Customer Feedback:")
        for feedback in self.feedbackList:
            print(f"- {feedback}")

def collect_feedback(feedbackManager: CustomerFeedbackManager):
    feedback = input("Insert customer feedback: ")
    feedbackManager.collect_feedback(feedback)

def init(account: Account):
    feedbackManager = CustomerFeedbackManager()
    feedbackMenu = OptionMenu("Customer Feedback")

    feedbackMenu.add_option("View Feedbacks", lambda: feedbackManager.view_feedback())
    feedbackMenu.add_option("Collect Feedback", lambda: collect_feedback(feedbackManager))

    feedbackMenu.process()