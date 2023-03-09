#!/usr/bin/env python3
"""
Index GEOIDs by the order in the points file.
- Need an index for each granularity that is run through Balzer.

For example:

$ scripts/index_geoids.py -s NC 

For documentation, type:

$ scripts/index_geoids.py -h

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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Convert pickled data to CSV format."""

    args: Namespace = parse_args()

    xx: str = args.state
    unit: str = "bg" if xx in ["CA", "OR"] else "vtd"

    ### CREATE THE INDEX ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    types: list = [str, int, float, float]
    vtd_points: list = read_typed_csv(rel_path, types)

    index_by_geoid: dict = {}
    for i, vtd in enumerate(vtd_points):
        index_by_geoid[vtd["GEOID"]] = i

    ### PICKLE THE RESULTS ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "index"], "_", "pickle"
    )
    write_pickle(rel_path, index_by_geoid)


if __name__ == "__main__":
    main()

### END ###
