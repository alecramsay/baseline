#!/usr/bin/env python3
#

"""
Create block-to-VTD and VTD-to-block mappings for FL.

For example:

$ scripts/extract_blocks_by_vtd_FL.py

For documentation, type:

$ scripts/extract_blocks_by_vtd_FL.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of VTDs (precincts) to blocks for FL."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="FL",
        help="The two-character state code (e.g., FL)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Create a dict of VTDs and their associated blocks."""

    args: Namespace = parse_args()

    xx: str = args.state
    if xx != "FL":
        raise ValueError(f"This script is only for FL!")

    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### READ THE CENSUS FILE & CREATE THE MAPPINGS ###

    if study_unit(xx) != "vtd":
        raise NotImplementedError("This state does not have VTDs. Use BGs instead.")

    vtd_blocks: dict[str, list[str]] = dict()
    block_vtd: list[dict] = list()

    rel_path: str = path_to_file([rawdata_dir, xx]) + file_name(
        ["blockmapping"], "_", "json"
    )
    abs_path: str = FileSpec(rel_path).abs_path
    block_vtd_mapping: dict[str, Any] = read_json(abs_path)

    for block, vtd in block_vtd_mapping.items():
        if vtd not in vtd_blocks:
            vtd_blocks[vtd] = list()

        vtd_blocks[vtd].append(block)
        block_vtd.append(
            {
                "BLOCK": block,
                "PRECINCT": vtd,
            }
        )

    pass

    ### PICKLE BLOCKS BY VTD ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "vtd", "blocks"], "_", "pickle"
    )
    write_pickle(rel_path, vtd_blocks)

    ### WRITE BLOCK-TO-VTD MAPPING TO A CSV ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "csv"
    )
    write_csv(
        rel_path,
        block_vtd,
        [
            "BLOCK",
            "PRECINCT",
        ],
    )

    pass


if __name__ == "__main__":
    main()

### END ###
