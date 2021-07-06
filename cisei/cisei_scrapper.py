from datetime import date, datetime
import re
from urllib.parse import urljoin
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests.sessions import Session
import csv
from time import sleep
import requests
from bs4 import BeautifulSoup
from tenacity import retry, wait_fixed
from os import path
from pydantic import BaseModel


class PersonalInfo(BaseModel):
    idx: int
    surname: str
    full_name: str
    age: str
    trip_date: date = None
    registration_place: str
    details: str


class CiseiRequestHandler:
    _DEFAULT_CONNECTION_TIMEOUT = 3
    _DEFAULT_RESPONSE_TIMEOUT = 3
    _URL = "http://www.ciseionline.it/portomondo/ricerca.asp"

    def __init__(self):
        self.timeout = (
            self._DEFAULT_CONNECTION_TIMEOUT,
            self._DEFAULT_RESPONSE_TIMEOUT,
        )
        self.retries = Retry(connect=5, read=2, redirect=5)

        self.session = self._init_session()

    def _init_session(self):
        session = Session()
        session.mount("http://", HTTPAdapter(max_retries=self.retries))
        session.mount("https://", HTTPAdapter(max_retries=self.retries))
        session.headers.update(
            {
                "User-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
            }
        )
        return session

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


def get_names_list():
    with open("cognomix/names.csv", mode="r") as f:
        names = csv.reader(f)
        names_list = []
        for name in names:
            names_list.append(name[0])
        return names_list


def get_person_info(td_list, name):
    idx = td_list[0].text

    age = re.search(r"\d+", td_list[2].text)
    age = age.group(0) if age is not None else ""

    full_name = re.findall(r"[A-Z]+", td_list[1].text)
    full_name = (
        " ".join(full_name).replace(name.upper() + " ", "").title()
        if full_name is not None
        else ""
    )

    trip_date = re.findall(r"\d{1,4}", td_list[3].text)
    trip_date = (
        datetime.strptime("-".join(trip_date), "%d-%m-%Y")
        if trip_date is not None
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
        details=details,
    )

    return person_info


def scrap_cisei():
    crh = CiseiRequestHandler()
    # names = get_names_list()
    names = ["Corsini"]  # TODO: Change to get_names_list
    for name in names:
        soup = crh.get_surname_soup(name)
        tr_list = soup.find("div", {"class": "box"}).find("center").find_all("tr")
        for tr in tr_list:
            td_list = tr.find_all("td", {"class": "tdesito"})
            if len(td_list) != 0:
                person_info = get_person_info(td_list, name)
                print(person_info)
