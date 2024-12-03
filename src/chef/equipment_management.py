from util.accounts import Account
from util.menu import OptionMenu

class Equipment:
    def __init__(self, name, issue, report_date, status="Pending"):
        self.name = name
        self.issue = issue
        self.report_date = report_date
        self.status = status
        self.equipmentLog = []

    def update_status(self, new_status):
        self.status = new_status

def display_equipment(equipment: Equipment):
    print (f"Equipment Name: {equipment.name}")
    print(f"Issue: {equipment.issue}")
    print(f"Reported On: {equipment.report_date}")
    print(f"Status: {equipment.status}")

def report_equipment_issue(name, issue, report_date):
   if not name or not issue or not report_date:
       print("All fields are required to report an issue.")
       return
   equipment = Equipment(name, issue, report_date)
   equipment.equipmentLog.append(equipment)
   print("\nEquipment issue reported successfully!")
   display_equipment(equipment)

def update_equipment_status(name, new_status):
    equipmentList: list[Equipment] = []
    for equipment in equipmentList:
        if equipment.name == name:
            equipment.update_status(new_status)
            print(f"\nThe status of '{name}' has been updated to '{new_status}'.")
            display_equipment(equipment)
            return
        print(f"\nNo equipment found with the name '{name}'.")

def view_equipment_logs(equipment: Equipment):
    if not equipment:
        print("\nNo equipment issues have been reported.")
    else:
        print("\n Equipment Logs")
        for equipmentLog in equipment.equipmentLog:
            display_equipment(equipment)

def main():
    while True:
        print("\nEquipment Management Menu")
        print("1. Report an Equipment Issue")
        print("2. Update Equipment Status")
        print("3. View Equipment Logs")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            name = input("Enter the equipment name: ")
            issue = input("Describe the issue: ")
            report_date = input("Enter the report date (YYYY-MM-DD): ")
            report_equipment_issue(name, issue, report_date)

        elif choice == "2":
            name = input("Enter the equipment name to update: ")
            new_status = input("Enter the new status (e.g., Resolved, In Progress): ")
            update_equipment_status(name, new_status)

        elif choice == "3":
            view_equipment_logs(None)

        elif choice =="4":
            print("\nExiting Equipment Management. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a valid option.")






def init(account: Account):
    equipment = Equipment("Name", None, "22-04-2023")
    equipment.equipmentLog.append("Issue here")


    pass