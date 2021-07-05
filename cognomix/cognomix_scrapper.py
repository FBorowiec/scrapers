from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup


LETTERE = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "I",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "Z",
]


def get_soup(letter, page_number):
    r = requests.get(
        "https://www.cognomix.it/origine-cognomi-italiani/"
        + letter
        + "/"
        + str(page_number),
        headers={
            "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
        },
    )
    r.raise_for_status()
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    return soup


def get_page_numbers(soup):
    page_content = soup.find_all("div", {"class": "text-center"})
    for content in page_content:
        if "Pagina" in content.text:
            return int(content.find_all("a", href=True)[-1].contents[0])


def scrap_cognomix():
    names_list = []
    for letter in LETTERE:
        soup = get_soup(letter=letter, page_number=1)
        pages = get_page_numbers(soup)
        for i in range(pages):
            soup = get_soup(letter=letter, page_number=i + 1)

            names_content_list = soup.find_all("div", {"class": "contenuto"})
            names = None
            for content in names_content_list:
                names_content = content.find("ul")
                if names_content is not None:
                    names = names_content

            for li in names.find_all("li"):
                names_list.append(li.text.split("-")[0][:-1])

            sleep(0.5)

    print(len(names_list))
