from datetime import date, datetime
import json
import re
from urllib.parse import urljoin
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests.sessions import Session
import csv
from typing import Optional, Dict
from time import sleep
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed
from pydantic import BaseModel, HttpUrl


class PersonalInfo(BaseModel):
    idx: int
    surname: str
    full_name: str
    age: Optional[int] = None
    trip_date: Optional[date]
    registration_place: str
    url: HttpUrl
    details: Optional[Dict]


class CiseiRequestHandler:
    _DEFAULT_CONNECTION_TIMEOUT = 3
    _DEFAULT_RESPONSE_TIMEOUT = 3
    _URL = "http://www.ciseionline.it/portomondo/ricerca.asp"
    _BASE_PERSON_URL = "http://www.ciseionline.it/portomondo/"
    _NEXT_PAGE_URL = "http://www.ciseionline.it/portomondo/tabelle.asp?primo=16"

    def __init__(self):
        self.timeout = (
            self._DEFAULT_CONNECTION_TIMEOUT,
            self._DEFAULT_RESPONSE_TIMEOUT,
        )

        self.session = self._init_session()

    def _init_session(self):
        session = Session()
        retries = Retry(connect=10, read=10, redirect=10)

        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        session.headers.update(
            {
                "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        )
        return session

    @retry(wait=wait_fixed(1))
    def get_surname_soup(self, surname: str):
        custom_header = {
            "input_cognome": surname,
            "input_nome": "",
            "input_dest": "al",
        }
        r = self.session.post(self._URL, custom_header)
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    @retry(wait=wait_fixed(1))
    def get_details_soup(self, details_url):
        r = self.session.get(details_url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    # TODO: fix this
    def get_next_page(self, soup):
        custom_header = {"ASPSESSIONIDSQQAABTC": "FEPJIJIBMFNLAOBGIJFKMACA"}
        # match = soup.find_all("a", href=re.compile(r".*tabelle.*"))
        # return match
        r = self.session.get(self._NEXT_PAGE_URL, custom_header)
        r.raise_for_status()
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        return soup

    @staticmethod
    def get_names_list():
        with open("cognomix/names.csv", mode="r") as f:
            names = csv.reader(f)
            names_list = []
            for name in names:
                names_list.append(name[0])
            return names_list

    def get_person_info(self, td_list, name):
        idx = td_list[0].text

        age = re.search(r"\d+", td_list[2].text)
        age = age.group(0) if age is not None else None

        full_name = re.findall(r"[A-Z]+", td_list[1].text)
        full_name = (
            " ".join(full_name).replace(name.upper() + " ", "").title()
            if full_name is not None
            else ""
        )

        trip_date = re.findall(r"\d{1,4}", td_list[3].text)
        trip_date = (
            datetime.strptime("-".join(trip_date), "%d-%m-%Y")
            if len(trip_date) != 0
            else None
        )

        registration_place = re.findall(r"\b[A-Z\w+]+", td_list[4].text)
        registration_place = (
            " ".join(registration_place) if registration_place is not None else ""
        )

        details = str(td_list[5].contents[1]).split('"')[1]

        person_info = PersonalInfo(
            idx=idx,
            surname=name,
            full_name=full_name,
            age=age,
            trip_date=trip_date,
            registration_place=registration_place,
            url=urljoin(self._BASE_PERSON_URL, details),
        )

        return person_info

    def get_person_details(self, person: PersonalInfo):
        soup = self.get_details_soup(person.url)
        tr_list = soup.find_all("td")
        details_dict = {}
        for tr in tr_list:
            raw_txt = re.sub(r"\\<[/]?[a-z]\\>", "", tr.text).splitlines()

            for line in raw_txt:
                try:
                    k, v = line.split(":")
                    key = k.strip()
                    value = v.strip()
                    if len(value) != 0 and value not in ["nd", "ND", "n.d.", "N.D."]:
                        details_dict[key] = value
                except ValueError:
                    pass

        return details_dict


def scrap_cisei():
    crh = CiseiRequestHandler()
    # names = get_names_list()
    names = ["Corsini"]  # TODO: Change to get_names_list
    for name in names:
        soup = crh.get_surname_soup(name)
        # print(crh.get_next_page(soup))
        tr_list = soup.find("div", {"class": "box"}).find("center").find_all("tr")
        for tr in tr_list:
            td_list = tr.find_all("td", {"class": "tdesito"})
            if len(td_list) != 0:
                person_info = crh.get_person_info(td_list, name)
                person_details = crh.get_person_details(person_info)
                person_info.details = person_details

                print(person_info)
                print()
        sleep(1)  # do not overload the server
