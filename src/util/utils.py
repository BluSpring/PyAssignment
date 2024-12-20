import time
from datetime import datetime

def get_current_time_millis() -> int:
    # time.time() returns a float in seconds, we want a milliseconds integer.
    return round(time.time() * 1000)

# Converts millisecond time to a formatted date and time, following the format DD/MM/YYYY HH:MM:SS.
def millis_to_formatted_date_time(milliseconds: int) -> str:
    date = datetime.fromtimestamp(milliseconds / 1000)

    return f"{date.day:02d}/{date.month:02d}/{date.year} {date.hour:02d}:{date.minute:02d}:{date.second:02d}"

# Upper-cases the first character of each word.
def proper_case(text: str) -> str:
    newText = ""

    # Split the sentence into words.
    for word in text.split(" "):
        # If the word is empty or simply whitespace, just add it onto the new text and ignore.
        if len(word.strip()) <= 0:
            newText += word
            continue

        # Uppercase the first character, and lowercase the rest of the word.
        newWord = word[0].upper() + word[1:].lower()

        # Add the word onto the new text.
        newText += newWord + ' '

    # Remove trailing spaces from the text.
    return newText.removesuffix(" ")

# Gets the current month.
def get_month() -> int:
    return datetime.now().month

# Gets the name of the current month.
def get_formatted_month(month: int) -> str:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    return months[month - 1]

# Gets the current month number from the name.
def get_month_from_formatted(monthName: str) -> int:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    for month in range(len(months)):
        if monthName.lower().strip() == months[month].lower():
            return month

    raise Exception(f"Invalid month name {monthName}!")

# Gets the current year.
def get_year() -> int:
    return datetime.now().year

# Formats the month and year into MM-YYYY.
def get_formatted_key(month: int, year: int) -> str:
    return f"{month:02d}-{year}"
