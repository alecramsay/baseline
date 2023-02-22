#!/usr/bin/env python3
#
# CONVERT PICKLED DATA TO CSV
#

"""
Convert pickled data to CSV format.

For example:

$ scripts/unpickle_to_csv.py -s NC -u vtd

For documentation, type:

$ scripts/unpickle_to_csv.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from typing import Any

from baseline import *

# TODO - Revise this to allow multiple unit granularities per call

### PARSE ARGS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Unpickle data to CSV format."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--units",
        default="vtd",
        help="The unit of granularity (e.g., vtd)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Convert pickled data to CSV format."""

    args: Namespace = parse_args()

    xx: str = args.state
    units: str = args.units

    state_dir: str = xx

    ### LOAD DATA ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, units, "data"], "_", "pickle"
    )
    collection: FeatureCollection = FeatureCollection(rel_path)

    ### WRITE DATA AS A CSV ###

    l: list = list()
    for f in collection.features:
        row: dict[str, int, int, int] = {
            "GEOID": f["geoid"],
            "POP": f["pop"],
            "X": f["xy"].x,
            "Y": f["xy"].y,
        }
        l.append(row)

    rel_path: str = path_to_file([data_dir, state_dir]) + file_name(
        [xx, cycle, units, "data"], "_", "csv"
    )
    write_csv(rel_path, l, ["GEOID", "POP", "X", "Y"], "{:.14f}")


if __name__ == "__main__":
    main()

### END ###
