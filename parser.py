import argparse
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Mr Lodge Scraper")
    auxiliary_parser = parser.add_argument_group()
    website_parser = auxiliary_parser.add_mutually_exclusive_group()
    auxiliary_parser.add_argument(
        "--output_folder",
        type=Path,
        help="Extract the scrapped data onto a csv file on your filesystem",
        required=False,
    )
    website_parser.add_argument(
        "--mr_lodge",
        help="Scrap data from current apartments available on Mr. Lodge",
        required=False,
        action="store_true",
    )
    website_parser.add_argument(
        "--cisei",
        help="Get italian emmigration data from ciseionline.it",
        required=False,
        action="store_true",
    )
    website_parser.add_argument(
        "--cognomix",
        help="Get most common italian surnames",
        required=False,
        action="store_true",
    )
    website_parser.add_argument(
        "--currencies_rates",
        help="Get current currencies rates values",
        required=False,
        action="store_true",
    )

    return parser.parse_args()
