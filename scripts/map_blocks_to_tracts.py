#!/usr/bin/env python3
#

"""
Convert a tract-assignment file for CA to a block-assignment file.

For example:

$ scripts/map_tracts_to_blocks.py -s CA

For documentation, type:

$ scripts/map_tracts_to_blocks.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of tracts to blocks."
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

    xx: str = args.state
    assert xx == "CA"

    verbose: bool = args.verbose

    ### READ A BAF & CREATE THE MAPPINGS ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "data"], "_", "csv"
    )
    types: list = [str, int, float, float]
    blocks: list = read_csv(rel_path, types)  # A list of dicts

    blocks_by_tract: dict[str, list] = dict()
    for row in blocks:
        block: str = row["GEOID"]
        tract: str = GeoID(block).tract

        if tract not in blocks_by_tract:
            blocks_by_tract[tract] = list()

        blocks_by_tract[tract].append(block)

    ### PICKLE THE RESULTS ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "tract", "blocks"], "_", "pickle"
    )
    write_pickle(rel_path, blocks_by_tract)

    pass


if __name__ == "__main__":
    main()

### END ###
