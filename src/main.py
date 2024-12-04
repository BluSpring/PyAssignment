import cashier
import chef
import customer
import manager
from util.menu import OptionMenu

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