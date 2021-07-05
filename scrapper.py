from os import path
from parser import parse_arguments
from cisei.cisei_scrapper import scrap_cisei
from cognomix.cognomix_scrapper import scrap_cognomix
from currencies_rates.currencies_rates_scrapper import scrap_currencies_rates
from mr_lodge.mr_lodge_scrapper import scrap_mr_lodge


def interface():
    args = parse_arguments()

    if args.mr_lodge:
        data = scrap_mr_lodge()

    if args.currencies_rates:
        data = scrap_currencies_rates()

    if args.cisei:
        data = scrap_cisei()

    if args.cognomix:
        data = scrap_cognomix()

    if args.output_folder:
        data.to_csv(path.join(args.output_folder, "output_data.csv"))


if __name__ == "__main__":
    interface()
