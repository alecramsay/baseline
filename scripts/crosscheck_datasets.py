#!/usr/bin/env python3
#

"""
Crosscheck data and adjacency pairs datasets for consistency.

For example:

$ scripts/crosscheck_datasets.py -s NC

For documentation, type:

$ scripts/crosscheck_datasets.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Crosscheck data and adjacency pairs datasets for consistency."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Crosscheck data and adjacency pairs datasets for consistency."""

    args: Namespace = parse_args()

    xx: str = args.state
    unit: str = "vtd"  # Change for CA & OR

    verbose: bool = args.verbose

    # Paths

    data_csv: str = full_path([data_dir, xx], [xx, cycle, "vtd", "data"])
    pairs_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "pairs"], "_", "csv"
    )
    index_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "index"], "_", "pickle"
    )

    # Reads

    data: list = read_csv(data_csv, [str, int, float, float])
    pairs: list = read_csv(pairs_path, [int, int])
    index: dict = read_pickle(index_path)

    print(f"Checking {xx} data and adjacency pairs datasets for consistency...")

    result: bool = datasets_are_consistent(data, pairs, index)

    if result:
        print(f"{xx} data and adjacency pairs datasets are consistent.")


if __name__ == "__main__":
    main()

### END ###
