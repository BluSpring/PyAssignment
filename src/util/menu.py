import os
from typing import Self, Callable


def _clear_screen():
    if os.name == "nt": # Windows uses "cls" to clear the console.
        os.system("cls")
    else: # Most other operating systems use "clear".
        os.system("clear")

class OptionMenu:
    name: str # Option menu name.
    description: str # Description
    _options: list[tuple[str, Callable]] # Internal value, used to map options to a function without being bound to a key/value pair.
    automaticallyExit: bool # Should the menu automatically exit after being completed?
    automaticallyClearScreen: bool # Should the menu automatically clear the screen?
    exiting: bool # If the menu is currently being exited. May be used as a sentinel value in while loops.

    def __init__(self: Self, name: str):
        self.name = name
        self.description = ""
        self._options = []
        self.automaticallyExit = False
        self.automaticallyClearScreen = True
        self.exiting = False

    # Allows us to easily add new options to the menu.
    def add_option(self: Self, name: str, option: Callable) -> Self:
        self._options.append((name, option))

        return self

    # Must be run after all options are added, to be able to display the menu to users.
    def process(self):
        print()
        print(f"---[  {self.name}  ]---")

        if self.description != "":
            print(self.description)

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
                self.exiting = True
                return
            elif value < 0 or value > len(self._options): # Check if the inserted value is within the bounds.
                print(f"Number is out of bounds! Number must be between 0 and {len(self._options)}!")
            else:
                option = self._options[value - 1]
                print()
                option[1]() # Invoke the callable option

            if not self.automaticallyExit:
                input("Press enter to continue...")
                if self.automaticallyClearScreen:
                    _clear_screen()  # Clear the terminal window.
                self.process() # After the option completes, re-run this function until the user exits.
            else:
                if self.automaticallyClearScreen:
                    _clear_screen()
        except ValueError: # If the user inputs an invalid number, just process it again.
            print("Invalid number!")
            self.process()
        except KeyboardInterrupt: # If the user pushes Ctrl+C, exit out of this loop.
            print("Received keyboard interrupt, exiting.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            # raise e