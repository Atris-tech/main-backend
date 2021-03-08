from bs4 import BeautifulSoup


def html_to_text(data):
    soup = BeautifulSoup(data, features="html5lib")
    return soup.get_text(strip=True, separator=" ")
