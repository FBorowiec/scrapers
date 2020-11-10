import requests
from bs4 import BeautifulSoup

def scrap_mr_lodge():
    r = requests.get("https://www.mrlodge.com/apartments-munich/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content

    soup = BeautifulSoup(c, "html.parser")

    # print(soup.prettify)

    apartments = soup.find_all("div", {"class":"mrlobject-list__item__content"})
    ap1 = apartments[0].find("span", {"class":"obj-rent"}).text.replace(".-", "").replace(",", "")
    return ap1