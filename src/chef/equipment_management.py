from util.accounts import Account

def init(account: Account):
    pass

class Equipment:
    def __init__(self, name, issue, report_date, status="Pending"):
        self.name = name
        self.issue = issue
        self.report_date = report_date
        self.status = status

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"Equipment: {self.name}, Issue: {self.issue}, Date: {self.report_date}, Status: {self.status}"

equipment_logs = []


    log = Equipment(name, issue, report_date)

    print(f"Equipment issue reported: {log}")

def update_equipment_status(name, new_status):
    for log in equipment_logs:


            print(f"Equipment {name} status updated to {new_status}")
            return
    print("Equipment not found.")

def view_equipment_logs():

    for log in equipment_logs:
        print(log)
