import difflib


def compare(str1, str2):
    return len([li for li in difflib.ndiff(str1, str2) if li[0] != ' '])