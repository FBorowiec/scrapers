import argparse
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Mr Lodge Scraper")
    parser.add_argument(
        "--mr_lodge", help="Scrap data from current apartments available on Mr. Lodge", required=True,  action="store_true"
    )

    return parser.parse_args()
