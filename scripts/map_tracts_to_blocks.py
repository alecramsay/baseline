#!/usr/bin/env python3
#

"""
Create a dict of tracts and their associated blocks for CA.
Use this to translate a tract-assignment file to a block-assignment file.

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
    assert xx == "CA"  # for CA only
    plan_type: str = "congress"  # for congress only
    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)

    # Unpickle blocks by tract

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "tract", "blocks"], "_", "pickle"
    )
    blocks_by_tract: dict = read_pickle(rel_path)

    # Read the tract-assignment file

    rel_path: str = path_to_file([maps_dir, xx]) + file_name(
        [map_label, "baseline", "100", "tracts"], "_", "csv"
    )
    types: list = [str, int]
    tract_assignments: list = read_csv(rel_path, types)  # A list of dicts

    # Map tract assignments to block assignments

    block_assignments: list = list()
    for tract_assignment in tract_assignments:
        tract: str = tract_assignment["GEOID"]
        district: int = tract_assignment["DISTRICT"]

        for block in blocks_by_tract[tract]:
            block_assignments.append({"GEOID": block, "DISTRICT": district})

    rel_path: str = path_to_file([maps_dir, xx]) + file_name(
        [map_label, "baseline", "100"], "_", "csv"
    )
    write_csv(rel_path, block_assignments, ["GEOID", "DISTRICT"])


if __name__ == "__main__":
    main()

### END ###
