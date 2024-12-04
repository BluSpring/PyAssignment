import math
from typing import Callable, TypeVar, Generic

from util.menu import OptionMenu

# Define generic typing
T = TypeVar("T")

class Manager(Generic[T]):
    def load(self):
        pass

    def save(self):
        pass

def create_pagination(manager: Manager[T], name: str, items: list[T], lineDisplay: Callable[[T], str], additionalOptions: Callable[[OptionMenu], None] | None, page: int):
    maxPages = math.ceil(len(items) / 10)
    # The index to use for printing the items
    itemsStart = page * 10

    # Only list up to a max of 10 items.
    totalToDisplay = min(10, len(items) - itemsStart)

    menu = OptionMenu(name)
    menu.automaticallyExit = True
    menu.description = ""

    for i in range(itemsStart, itemsStart + totalToDisplay):
        item = items[i]
        menu.description += f"\n  {i + 1}. {lineDisplay(item)}"

    menu.description += f"\n\nShowing {totalToDisplay} items out of {len(items)}."
    menu.description += f"\nPage {page + 1} / {maxPages}"

    if additionalOptions is not None:
        additionalOptions(menu)

    if page > 0:
        menu.add_option("Previous Page", lambda: create_pagination(manager, name, items, lineDisplay, additionalOptions, page - 1))

    if page < maxPages - 1:
        menu.add_option("Next Page", lambda: create_pagination(manager, name, items, lineDisplay, additionalOptions, page + 1))

    menu.process()