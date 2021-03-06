import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrap_mr_lodge():
    for page in range(0, 10, 1):
        r = requests.get(
            "https://www.mrlodge.com/apartments-munich/?mrl_ft%5Bfd%5D=3&amp;mrl_ft%5Bpage%5D="
            + str(page),
            headers={
                "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
            },
        )
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")

        apartments = soup.find_all("div", {"class": "mrlobject-list__item__content"})

        list_of_aparments = []
        for apartment in apartments:
            apart_dict = {}
            try:
                apart_dict["Rent"] = (
                    apartment.find("span", {"class": "obj-rent"})
                    .text.replace(".-", "")
                    .replace(",", "")
                )
            except:
                apart_dict["Rent"] = None
            try:
                apart_dict["Location"] = apartment.find(
                    "div", {"class": "obj-smallinfo"}
                ).text
            except:
                apart_dict["Location"] = None
            try:
                apart_dict["Rooms"] = float(
                    apartment.find("span", {"class": "obj-room"})
                    .text.replace(" ", "")
                    .replace("rooms", "")
                    .replace("room", "")
                )
            except:
                apart_dict["Rooms"] = None
            try:
                apart_dict["Area"] = apartment.find("span", {"class": "obj-area"}).text
            except:
                apart_dict["Area"] = None

            list_of_aparments.append(apart_dict)

        return pd.DataFrame(list_of_aparments)
