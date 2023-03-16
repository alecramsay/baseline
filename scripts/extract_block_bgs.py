#!/usr/bin/env python3
#

"""
Create a dict of blocks and their associated BGs (for CA & OR).

For example:

$ scripts/extract_block_bgs.py -s CA

For documentation, type:

$ scripts/extract_block_bgs.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of BGs to blocks."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="CA",
        help="The two-character state code (e.g., CA)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Create a dict of BGs and their associated blocks."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = STATE_FIPS

    xx: str = args.state
    fips: str = fips_map[xx]

    verbose: bool = args.verbose

    ### READ A BAF & CREATE THE MAPPINGS ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "assignments"], "_", "csv"
    )
    types: list = [str, int]
    block_assignments: list = read_csv(
        rel_path, types
    )  # A list of dicts like {'GEOID20': '371139703032008', 'District': 11}

    block_bg: dict[str, str] = dict()
    for row in block_assignments:
        block: str = row["GEOID20"]
        bg: str = GeoID(block).bg
        block_bg[block] = bg

    ### PICKLE THE RESULTS ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "bg"], "_", "pickle"
    )
    write_pickle(rel_path, block_bg)

    pass


if __name__ == "__main__":
    main()

### END ###
