import csv
from typing import List


def get_names_list() -> List[str]:
    names_list, jewish_names_list = [], []
    with open("cognomix/names.csv", mode="r") as f:
        names = csv.reader(f)
        names_list = []
        for name in names:
            names_list.append(name[0])

    with open("cognomix/jewish_italian_names.csv", mode="r") as f:
        jewish_names = csv.reader(f)
        jewish_names_list = []
        for jname in jewish_names:
            jewish_names_list.append(jname[0])

    all_names = sorted(set(names_list + jewish_names_list))
    return all_names
