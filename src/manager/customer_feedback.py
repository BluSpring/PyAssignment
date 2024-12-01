from util.accounts import Account

# Customer Feedback - Manager
class CustomerFeedbackManager:
    def _init_(self):
        self.feedback_list = []

    def collect_feedback(self, feedback):
        self.feedback_list.append(feedback)
        print(f"Feedback collected: {feedback}")

    def view_feedback(self):
        print("Customer Feedback:")
        for feedback in self.feedback_list:
            print(f"- {feedback}")

def init(account: Account):
    pass