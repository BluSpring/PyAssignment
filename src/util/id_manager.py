import json

class IdManager:
    ids: dict[str, int]

    def save(self):
        with open("ids.json", "w") as file:
            json.dump(self.ids, file, indent=4)

    def load(self):
        try:
            with open("ids.json", "r") as file:
                data = json.load(file)
                self.ids = data
        except FileNotFoundError:
            # Ignore non-existing files
            pass

    def get_id(self, name: str) -> int:
        if self.ids[name] is None:
            self.ids[name] = 0

        return self.ids[name]

    def get_and_increment_id(self, name: str) -> int:
        currentId = self.get_id(name)
        self.ids[name] = currentId + 1
        self.save()

        return currentId