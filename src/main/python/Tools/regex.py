import re


def VerifAdresse(text):
    return re.match("^[a-zA-Z0-9]+([ -][a-zA-Z0-9]+)*$", text)


def VerifISIN(text):
    return re.match("^[a-zA-Z0-9]{12}$", text)


def VerifFloat(text):
    try:
        float(text)
        return True
    except ValueError:
        return False