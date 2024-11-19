from typing import Self, Callable
import os

def _clear_screen():
    if os.name == "nt": # Windows uses "cls" to clear the console.
        os.system("cls")
    else: # Most other operating systems use "clear".
        os.system("clear")

class OptionMenu:
    name: str = ""
    description: str = ""
    _options: list[tuple[str, Callable]] = []

    def __init__(self: Self, name: str):
        self.name = name

    # Allows us to easily add new options to the menu.
    def add_option(self: Self, name: str, option: Callable) -> Self:
        self._options.append((name, option))

        return self

    # Must be run after all options are added, to be able to display the menu to users.
    def process(self):
        print()
        print(f"---[  {self.name}  ]---")

        if self.description != "":
            print(self.description.strip()) # strip to ensure there is no extra erroneous whitespace.

        print()

        # List out all options with numbers for the user to select.
        for i, option in enumerate(self._options):
            print(f" {i + 1}. {option[0]}")

        print()
        print(" 0. Exit")

        try:
            print()
            value = int(input("Enter a number: "))

            if value == 0: # Exit if the value is 0.
                print("Exiting...")
                return
            elif value < 0 or value > len(self._options): # Check if the inserted value is within the bounds.
                print(f"Number is out of bounds! Number must be between 0 and {len(self._options)}!")
            else:
                option = self._options[value - 1]
                print()
                option[1]() # Invoke the callable option

            input("Press enter to continue...")
            _clear_screen() # Clear the terminal window.
            self.process() # After the option completes, re-run this function until the user exits.
        except ValueError: # If the user inputs an invalid number, just process it again.
            print("Invalid number!")
            self.process()
        except KeyboardInterrupt: # If the user pushes Ctrl+C, exit out of this loop.
            print("Received keyboard interrupt, exiting.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")