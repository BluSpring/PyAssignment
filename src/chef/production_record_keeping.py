import json
import operator

from util.accounts import Account
from util.dishes import DishManager
from util.id_manager import IdManager
from util.menu import OptionMenu
from util.pagination import Manager, create_pagination, ManagerSerializer
from util.utils import millis_to_formatted_date_time, get_current_time_millis


class ProductionRecord:
    dishName: str # The name of the produced dish
    quantity: int # Total quantity of dishes produced in the batch
    batchNumber: int # The batch number.
    productionTimestamp: int # The timestamp, in milliseconds, of when the batch was produced

    def __init__(self, dishName, quantity, batchNumber, productionTimestamp):
        self.dishName = dishName
        self.quantity = quantity
        self.batchNumber = batchNumber
        self.productionTimestamp = productionTimestamp

    # Get the expiry date of the batch.
    def get_expiry_timestamp(self):
        return self.productionTimestamp + 2.592e+8 # 3 days

def decode_item(obj: dict) -> ProductionRecord:
    return ProductionRecord(obj["dishName"], obj["quantity"], obj["batchNumber"], obj["productionTimestamp"])

class ProductionRecordManager(Manager[ProductionRecord]):
    records: list[ProductionRecord] # List of produced records

    def __init__(self):
        self.records = []
        self.load()

    def save(self):
        with open("production.json", "w") as file:
            json.dump(self.records, file, indent = 4, cls = ManagerSerializer)

    def load(self):
        try:
            with open("production.json", "r") as file:
                data = json.load(file, object_hook = decode_item)
                self.records = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    # Gets the batch by the specific record ID.
    def get_batch_by_id(self, id: int) -> ProductionRecord | None:
        for record in self.records:
            if record.batchNumber == id:
                return record

        return None

def init(account: Account):
    recordManager = ProductionRecordManager()
    menu = OptionMenu("Production Records")

    menu.add_option("View Records", lambda: view_production_records(recordManager))
    menu.add_option("Log Production Record", lambda: handle_log_record(recordManager))

    menu.process()

def handle_log_record(recordManager: ProductionRecordManager):
    dishManager = DishManager()
    idManager = IdManager()

    dishName = input("Insert a dish name: ")
    dish = dishManager.get_dish_lenient(dishName)

    if dish is None:
        raise Exception("No dish exists by that name!")

    quantity = int(input("Insert a quantity: "))

    if quantity <= 0:
        raise Exception("Production quantity must be higher than 0!")

    id = idManager.get_and_increment_id("production")
    record = ProductionRecord(dishName, quantity, id, get_current_time_millis())

    recordManager.records.append(record)
    print(f"Production logged for Batch #{record.batchNumber}.")


def view_production_records(recordManager: ProductionRecordManager):
    # Create a copy of the list of records, sorted from last produced to first produced.
    records = list(recordManager.records)
    records.sort(key = operator.attrgetter("productionTimestamp"), reverse = True)

    create_pagination(recordManager, "Production Records", records, (lambda record: f"Batch #{record.batchNumber}, creating {record.quantity} x {record.dishName}, expiring on {millis_to_formatted_date_time(record.get_expiry_timestamp())}"), None, 0)
