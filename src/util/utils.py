import time
from datetime import datetime

def get_current_time_millis() -> int:
    # time.time() returns a float in seconds, we want a milliseconds integer.
    return round(time.time() * 1000)

def millis_to_formatted_date_time(milliseconds: int) -> str:
    date = datetime.fromtimestamp(milliseconds / 1000)

    return f"{date.day}/{date.month}/{date.year} {date.hour}:{date.minute}:{date.second}"

# Upper-cases the first character of each word.
def proper_case(text: str) -> str:
    newText = ""

    for word in text.split(" "):
        if len(word.strip()) <= 0:
            newText += word
            continue

        newWord = word[0].upper() + word[1:].lower()
        newText += newWord

    return newText