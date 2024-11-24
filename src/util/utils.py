import time

def get_current_time_millis() -> int:
    # time.time() returns a float in seconds, we want a milliseconds integer.
    return round(time.time() * 1000)

# Upper-cases the first character of each word.
def proper_case(text: str) -> str:
    newText = ""

    for word in text.split(" "):
        newWord = word[0].upper() + word[1:].lower()
        newText += newWord

    return newText