import json
import pandas as pd
from urllib.request import urlopen


def scrap_currencies_rates(base="USD"):
    with urlopen("https://api.exchangeratesapi.io/latest?base=" + base) as response:
        source = response.read()

    data = json.loads(source)

    currencies = []
    for item in data["rates"]:
        currency_rates = {}
        name = item
        price = data["rates"][item]
        currency_rates[name] = price
        currencies.append(currency_rates)

    print(currencies)

    return pd.DataFrame(currencies)
