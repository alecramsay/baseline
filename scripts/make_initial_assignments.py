#!/usr/bin/env python3
#

"""
Make initial assignments

For example:

$ scripts/make_initial_assignments.py -s NC -v

For documentation, type:

$ scripts/make_initial_assignments.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

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
    """Make initial assignments."""

    args: Namespace = parse_args()
    xx: str = args.state
    unit: str = "vtd"

    verbose: bool = args.verbose

    # Load the block-to-VTD (temp/NC_2020_block_vtd.pickle)

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "pickle"
    )
    vtd_by_block: dict = read_pickle(rel_path)

    # Load the block population file for NC (temp/NC_2020_block_pop.pickle)

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "pop"], "_", "pickle"
    )
    pop_by_block: dict = read_pickle(rel_path)

    # Map VTD geoids to index offsets, using the points file (data/NC/NC_2020_vtd_data.csv)

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "data"], "_", "csv"
    )
    types: list = [str, int, float, float]
    vtd_points: list = read_typed_csv(rel_path, types)

    # TODO - Create geoid_to_index mapping

    # Read the BAF for the official NC map (data/NC/NC_2020_block_assignments.csv)

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "assignments"], "_", "csv"
    )
    types: list = [str, int]
    block_assignments: list = read_typed_csv(
        rel_path, types
    )  # A list of dicts like {'GEOID20': '371139703032008', 'District': 11}

    # TODO - Loop over the BAF, aggregating the block populations by VTD

    # TODO - Write the results to initial.csv

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###
