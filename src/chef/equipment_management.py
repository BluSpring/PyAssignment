import json
import operator

from util.accounts import Account
from util.id_manager import IdManager
from util.menu import OptionMenu
from util.pagination import Manager, create_pagination, ManagerSerializer
from util.utils import millis_to_formatted_date_time, get_current_time_millis, proper_case


class Equipment:
    name: str # Equipment name
    issue: str # The equipment issue
    issueId: int # The issue ID
    reportTimestamp: int # The timestamp of the issue being reported, in milliseconds.
    reporter: str # The username of the account reporting the issue.
    status: str # The current status. Valid values: "pending", "identified", "fixed", "replaced", "invalid".

    def __init__(self, name, issue, issueId, reportTimestamp, reporter, status = "Pending"):
        self.name = name
        self.issue = issue
        self.issueId = issueId
        self.reporter = reporter
        self.reportTimestamp = reportTimestamp
        self.status = status

    def display_formatted(self):
        print(f"Equipment Name: {self.name}")
        print(f"Issue #{self.issueId}: {self.issue}")
        print(f"Reported On: {millis_to_formatted_date_time(self.reportTimestamp)}")
        print(f"Status: {self.status}")

def validate_status(status: str):
    if status != "pending" and status != "identified" and status != "fixed" and status != "replaced" and status != "invalid":
        raise Exception(f"Invalid status {status}!")

def decode_equipment(obj: dict) -> Equipment:
    return Equipment(obj["name"], obj["issue"], obj["reporter"], obj["reportTimestamp"], obj["status"])

class EquipmentManager(Manager[Equipment]):
    equipment: list[Equipment]

    def __init__(self):
        self.equipment = []

    def save(self):
        with open("equipment.json", "w") as file:
            json.dump(self.equipment, file, indent = 4, cls = ManagerSerializer)

    def load(self):
        try:
            with open("equipment.json", "r") as file:
                data = json.load(file, object_hook = decode_equipment)
                self.equipment = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    # Gets the equipment name, without being case-sensitive or whitespace-sensitive.
    def get_equipment_lenient(self, name: str) -> list[Equipment]:
        equipmentList: list[Equipment] = []

        for equipment in self.equipment:
            if equipment.name.lower().strip() == name.lower().strip():
                equipmentList.append(equipment)

        return equipmentList

    # Gets the issue by the issue ID.
    def get_issue(self, id: int) -> Equipment | None:
        for equipment in self.equipment:
            if equipment.issueId == id:
                return equipment

        return None

def update_equipment_status(equipmentManager: EquipmentManager, equipment: Equipment, newStatus: str):
    equipment.status = newStatus
    equipmentManager.save()

def handle_report_issue(equipmentManager: EquipmentManager, account: Account):
    name = input("Insert the equipment name: ")
    issue = input("Insert the issue: ")

    idManager = IdManager()
    id = idManager.get_and_increment_id("issue")

    equipment = Equipment(name, issue, id, get_current_time_millis(), account.username)
    equipmentManager.equipment.append(equipment)
    equipmentManager.save()

    print(f"Equipment issue #{id} reported successfully!")

def handle_update_status(equipmentManager: EquipmentManager):
    id = int(input("Insert the equipment issue ID: "))
    equipment = equipmentManager.get_issue(id)

    statusMenu = OptionMenu("Select Issue Status")
    statusMenu.automaticallyExit = True

    for status in ["pending", "identified", "fixed", "replaced", "invalid"]:
        statusMenu.add_option(proper_case(status), lambda: update_equipment_status(equipmentManager, equipment, status))

    statusMenu.process()

def handle_view_logs(equipmentManager: EquipmentManager):
    name = input("Insert the equipment name: ")
    equipmentList = equipmentManager.get_equipment_lenient(name)

    if len(equipmentList) <= 0:
        raise Exception("No equipment by that name had any issues reported!")

    # Sort by latest issue to earliest issue.
    equipmentList.sort(key = operator.attrgetter("reportTimestamp"), reverse = True)

    create_pagination(equipmentManager, f"Equipment Issue Logs for {name}", equipmentList, (lambda equipment: f"Issue #{equipment.issueId} (reported by {equipment.reporter} on {millis_to_formatted_date_time(equipment.reportTimestamp)}) - {proper_case(equipment.status)}"), None, 0)

def init(account: Account):
    equipmentManager = EquipmentManager()
    menu = OptionMenu("Equipment Management Menu")

    menu.add_option("Report an Equipment Issue", lambda: handle_report_issue(equipmentManager, account))
    menu.add_option("Update Equipment Status", lambda: handle_update_status(equipmentManager))
    menu.add_option("View Equipment Logs", lambda: handle_view_logs(equipmentManager))

    menu.process()