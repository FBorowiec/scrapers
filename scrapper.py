from os import path
import pandas as pd
from parser import parse_arguments
from mr_lodge.mr_lodge_scrapper import scrap_mr_lodge


def interface():
    args = parse_arguments()

    if args.mr_lodge:
        data = scrap_mr_lodge()

    if args.output_folder:
        data.to_csv(path.join(args.output_folder, "output_data.csv"))


if __name__ == "__main__":
    interface()
