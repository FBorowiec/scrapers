import csv
from time import sleep
import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed
from os import path


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


@retry(wait=wait_fixed(1))
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
            if len(content.find_all("a", href=True)) != 0:
                return int(content.find_all("a", href=True)[-1].contents[0])
            else:
                return 1


def write_csv(names_list):
    file_path = path.expanduser("~/Downloads/names.csv")
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(names_list)


def scrap_cognomix():
    names_list = []
    for letter in LETTERE:
        soup = get_soup(letter=letter, page_number=1)
        pages = get_page_numbers(soup)
        for i in range(pages):
            print(f"Parsing {letter}, page: {i+1}")
            soup = get_soup(letter=letter, page_number=i + 1)

            names_content_list = soup.find_all("div", {"class": "contenuto"})
            names = None
            for content in names_content_list:
                names_content = content.find("ul")
                if names_content is not None:
                    names = names_content

            for li in names.find_all("li"):
                names_list.append([li.text.split("-")[0][:-1]])

            sleep(1)

    write_csv(names_list)
