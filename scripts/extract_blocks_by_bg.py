#!/usr/bin/env python3
#

"""
Create block-to-bg and bg-to-block mappings (for CA, OR, and WV).

For example:

$ scripts/extract_blocks_by_bg.py -s OR

For documentation, type:

$ scripts/extract_blocks_by_bg.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create block-to-bg and bg-to-block mappings."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="OR",
        help="The two-character state code (e.g., OR)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Create block-to-bg and bg-to-block mappings."""

    args: Namespace = parse_args()

    xx: str = args.state
    unit: str = study_unit(xx)

    verbose: bool = args.verbose

    ### READ A BAF & CREATE THE MAPPINGS ###

    if study_unit(xx) != "bg":
        raise NotImplementedError("This state does not use BGs. Use VTDs instead.")

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", "data"], "_", "csv"
    )

    bg_blocks: dict[str, list[str]] = dict()
    block_bg: list[dict] = list()

    types: list = [str, int, float, float]
    blocks: list = read_csv(rel_path, types)  # A list of dicts

    for row in blocks:
        block: str = row["GEOID"]
        bg: str = GeoID(block).bg

        if bg not in bg_blocks:
            bg_blocks[bg] = list()

        bg_blocks[bg].append(block)
        block_bg.append(
            {
                "BLOCK": block,
                "PRECINCT": bg,
            }
        )

    pass

    ### PICKLE BLOCKS BY VTD ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, unit, "blocks"], "_", "pickle"
    )
    write_pickle(rel_path, bg_blocks)

    ### WRITE BLOCK-TO-VTD MAPPING TO A CSV ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "block", unit], "_", "csv"
    )
    write_csv(
        rel_path,
        block_bg,
        [
            "BLOCK",
            "PRECINCT",
        ],
    )
    pass


if __name__ == "__main__":
    main()

### END ###
