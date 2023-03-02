#!/usr/bin/env python3
#

"""
Equalize district populations.

For example:

$ scripts/equalize_districts.py -s NC

For documentation, type:

$ scripts/equalize_districts.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Equalize district populations."
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
    """Equalize district populations."""

    args: Namespace = parse_args()
    fips_map: dict[str, str] = make_state_codes()
    xx: str = args.state
    fips: str = fips_map[xx]

    unit: str = "vtd"

    verbose: bool = args.verbose

    # Load the precinct data

    data_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "data"], "_", "pickle"
    )
    features: list[Feature] = read_pickle(data_path)
    pop_by_geoid: dict[str, int] = {f["geoid"]: f["pop"] for f in features}
    del features

    # TODO - Load the graph

    # TODO - Load the precinct-assignment file

    # TODO - Compute a district adjacency graph

    # TODO - Compute the population balance point

    # TODO - Compute the district populations

    # TODO - Split precincts to equalize district populations

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
