#!/usr/bin/env python3
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
        "-w", "--water", dest="water", action="store_true", help="Water-only precincts"
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
    water: bool = args.water

    ### LOAD DATA ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, units, "data"], "_", "pickle"
    )
    collection: FeatureCollection = FeatureCollection(rel_path)

    water_precincts: list = list()
    if water:
        rel_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, "water_only"], "_", "csv"
        )  # GEOID,ALAND,AWATER
        types: list = [str, int, int]
        water_precincts = [row["GEOID"] for row in read_typed_csv(rel_path, types)]
        print(f"# of water-only precincts: {len(water_precincts)}")

    ### WRITE DATA AS A CSV ###

    l: list = list()
    for f in collection.features:
        row: dict = {
            "GEOID": f["geoid"],
            "POP": f["pop"],
            "X": f["xy"].x,
            "Y": f["xy"].y,
        }
        if f in water_precincts:
            print(f"Removing water-only precinct {f['geoid']}")
            continue
        else:
            l.append(row)

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, units, "data"], "_", "csv"
    )
    write_csv(rel_path, l, ["GEOID", "POP", "X", "Y"], precision="{:.14f}")


if __name__ == "__main__":
    main()

### END ###
