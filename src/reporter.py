#!/usr/bin/env python3
"""
Ingest list of debts.
Determine which debts to pay in order,
and how long the total payout will be.
"""
# import math
import json
from operator import itemgetter
from pathlib import Path
from argparse import ArgumentParser
import sys


def _parse_args(args):
    """Parse inputs."""
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--input-file",
        required=True,
        help="File path to json input file.",
    )

    return parser.parse_args(args)


def find_in_mapping(sequence, key, value):
    """
    Search a sequence of mappings for one with a matching key-value pair.

    Only searches one level deep.

    Args:
        sequence (list(dict)): Sequence of mappings.
        key: Key to match.
        value: value to match

    Returns:
        The first matching mapping, or ``None`` if no such mapping exists.
    """
    mapping = None
    for map_value in sequence:
        try:
            if map_value[key] == value:
                mapping = map_value[key]
        except (KeyError, TypeError):
            pass
    return mapping


def sort_mappings(mappings, key, reverse=False):
    """Sort a sequence of mappings by a common key.

    Every mapping in the sequence must have the specified key, and all values
    corresponding to that key should be the same data type.

    .. warning::
        Providing a sequence that does not conform to the above criteria may
        result in undefined behavior.

    Args:
        mappings (list(dict)): Sequence of mappings.
        key (str): Common key.
        reverse (bool): Sort in reverse (descending) order.

    Returns:
        list(dict): sequence sorted by the specified common key.
    """
    return sorted(mappings, key=itemgetter(key), reverse=reverse)


def sort_debts(data):
    """Sort debts, ascending"""
    debts = list(data["debts"])

    return sort_mappings(mappings=debts, key="total", reverse=False)


def get_input(input_file):
    """Retrieve debt file."""
    data = {}
    with open(input_file, mode="r") as file:
        data = json.load(file)
    return data


def main():
    """Do Main Method"""
    args = _parse_args(sys.argv[1:])
    data = get_input(Path(args.input_file).resolve())
    output = Path(args.input_file.replace(".json", "_result.txt")).resolve()
    output.touch(mode=0o664, exist_ok=True)
    sorted_debts = sort_debts(data)

    rolling_total = 0
    with open(output, mode="w", newline="") as out_file:
        for debt in sorted_debts:
            out_file.write(
                f"Payoff {debt['name']}.\n"
                f"Total: {debt['total']}.\n"
                f"Original monthly payment: ${debt['payment']}."
            )
            suggested = (
                int(debt["payment"])
                + (int(debt["payment"]) * 0.10)
                + rolling_total
            )
            out_file.write(f"Suggested monthly payment: {suggested}.\n")
            rolling_total += suggested


if __name__ == "__main__":
    main()
