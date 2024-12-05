import cashier
import chef
import customer
import manager
from util.menu import OptionMenu

def main():
    print("--[  Amar's Restaurant  ]--")

    # Create the starting menu screen.
    selection = OptionMenu(name = "Select Login Type")
    selection.description = "Welcome to Amar's Restaurant's ordering and management system!"
    selection.description += "\nPlease select your corresponding login type to continue."

    # Add all login types as options, with their initializing functions to be executed when selected.
    selection.add_option("Manager", manager.init)
    selection.add_option("Chef", chef.init)
    selection.add_option("Cashier", cashier.init)
    selection.add_option("Customer", customer.init)

    # Display the menu onto the screen
    selection.process()

# If the file was run directly here, just allow it.
# The main() function was added so it could be called by the root main.py, as otherwise the program may not work correctly
# if it was run directly here, unless the working directory was manually set to the root directory.
if __name__ == "__main__":
    main()