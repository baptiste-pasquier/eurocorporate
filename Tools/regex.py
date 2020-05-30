import re

def VerifAdresse(text):
    return re.match("^[a-zA-Z0-9]+([ -][a-zA-Z0-9]+)*$", text)