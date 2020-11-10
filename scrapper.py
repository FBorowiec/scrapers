from parser import parse_arguments
from mr_lodge.mr_lodge_scrapper import scrap_mr_lodge


def interface():
    args = parse_arguments()

    if args.mr_lodge:
        print("mr lodge")
        print(scrap_mr_lodge())

if __name__ == "__main__":
    interface()
