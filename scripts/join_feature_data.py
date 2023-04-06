#!/usr/bin/env python3
#

"""
Join feature population and xy data by geoid in a list of dicts.

For example:

$ scripts/join_feature_data.py -s NC -p

For documentation, type:

$ scripts/join_feature_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Join feature population and xy data by geoid."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--tract",
        dest="tract",
        action="store_true",
        help="Generate tract-level data",
    )
    parser.add_argument(
        "-g", "--bg", dest="bg", action="store_true", help="Generate BG-level data"
    )
    parser.add_argument(
        "-p",
        "--precinct",
        dest="precinct",
        action="store_true",
        help="Generate VTD-level data",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Join feature population and xy data by geoid."""

    args: Namespace = parse_args()

    xx: str = args.state

    tracts: bool = args.tract
    bgs: bool = args.bg
    blocks: bool = True  # args.block
    vtds: bool = args.precinct

    verbose: bool = args.verbose

    ### JOIN THE POPULATION & COORDINATE DATA BY GEOID ###

    units: list[str] = list()
    if blocks:
        units.append("block")
    if tracts:
        units.append("tract")
    if bgs:
        units.append("bg")
    if vtds:
        units.append("vtd")

    for unit in units:
        pop_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, unit, "pop"], "_", "pickle"
        )
        xy_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, unit, "xy"], "_", "pickle"
        )

        pop: dict = read_pickle(pop_path)
        xy: dict = read_pickle(xy_path)

        features: list[Feature] = list()

        for geoid, population in pop.items():
            if geoid not in xy:
                print(f"Missing xy data for {geoid} (pop: {population}))")
                continue
            features.append(
                {"geoid": geoid, "pop": population, "xy": xy[geoid], "district": 0}
            )

        join_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, unit, "data"], "_", "pickle"
        )
        write_pickle(join_path, features)


if __name__ == "__main__":
    main()

### END ###
