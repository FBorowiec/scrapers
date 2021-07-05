import pandas as pd
import requests
from bs4 import BeautifulSoup

LETTERE = ["A"]
# "B",
# "C",
# "D",
# "E",
# "F",
# "G",
# "I",
# "L",
# "M",
# "N",
# "O",
# "P",
# "Q",
# "R",
# "S",
# "T",
# "U",
# "V",
# "Z",
# ]


def get_soup(letter):
    r = requests.get(
        "https://www.cognomix.it/origine-cognomi-italiani/" + letter,
        headers={
            "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
        },
    )
    r.raise_for_status()
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    return soup


# def get_page_numbers(soup):


def scrap_cognomix():
    names_list = []
    for letter in LETTERE:
        soup = get_soup(letter)

        names_content_list = soup.find_all("div", {"class": "contenuto"})
        names = None
        for content in names_content_list:
            names_content = content.find("ul")
            if names_content is not None:
                names = names_content

        for li in names.find_all("li"):
            names_list.append(li.text.split("-")[0][:-1])

        print(names_list)

        # list_of_names = []
        # for name in names:
        #     name.find("span", {"class": "obj-rent"})
        #     apart_dict = {}
        #     try:
        #         apart_dict["Rent"] = (
        #             .text.replace(".-", "")
        #             .replace(",", "")
        #         )
        #     except:
        #         apart_dict["Rent"] = None
        #     try:
        #         apart_dict["Location"] = apartment.find(
        #             "div", {"class": "obj-smallinfo"}
        #         ).text
        #     except:
        #         apart_dict["Location"] = None
        #     try:
        #         apart_dict["Rooms"] = float(
        #             apartment.find("span", {"class": "obj-room"})
        #             .text.replace(" ", "")
        #             .replace("rooms", "")
        #             .replace("room", "")
        #         )
        #     except:
        #         apart_dict["Rooms"] = None
        #     try:
        #         apart_dict["Area"] = apartment.find("span", {"class": "obj-area"}).text
        #     except:
        #         apart_dict["Area"] = None

        #     list_of_aparments.append(apart_dict)

        # return pd.DataFrame(list_of_aparments)
