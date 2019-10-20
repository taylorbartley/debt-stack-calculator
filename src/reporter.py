#!/usr/bin/env python3
"""
Ingest list of debts.
Determine which debts to pay in order,
and how long the total payout will be.
"""

import copy
import json

# import argparse


def get_input(input_file):
    """Retrieve debt file."""
    data = {}
    with open(input_file, mode="r") as file:
        data = json.load(file)
    return data


def sort_debts(data):
    """Sort debts, ascending"""
    temp_list = []
    temp_total = 0

    for debt, value in data.items():
        temp_list.append({debt: value})

    print(temp_list)

    for debt in temp_list:
        for keys in debt:
            mapping = debt[keys]
            temp_total = mapping["total"]
            print(temp_total)
            # for item, v in mapping.items():
            #     print(v)
            # print(keys)


def main():
    """Do Main Method"""
    data = dict(get_input("input/input.json"))

    sort_debts(data)
    # print(sorted_debts)


if __name__ == "__main__":
    main()
