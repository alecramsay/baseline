#!/usr/bin/env python3
#

"""
Create block-to-VTD and VTD-to-block mappings.

For example:

$ scripts/extract_blocks_by_vtd.py -s NC

For documentation, type:

$ scripts/extract_blocks_by_vtd.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of VTDs (precincts) to blocks."
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
    """Create a dict of VTDs and their associated blocks."""

    args: Namespace = parse_args()

    xx: str = args.state
    if not is_study_state(xx):
        raise ValueError(f"State {xx} is not part of the study.")

    verbose: bool = args.verbose

    # Debug

    # xx = "FL"

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### READ THE CENSUS FILE & CREATE THE MAPPINGS ###

    if study_unit(xx) != "vtd":
        raise NotImplementedError("This state does not have VTDs. Use BGs instead.")

    rel_path: str = path_to_file([rawdata_dir, xx]) + file_name(
        ["BlockAssign", f"ST{fips}", xx, "VTD"], "_", "txt"
    )

    vtd_blocks: dict[str, list[str]] = dict()
    block_vtd: list[dict] = list()

    abs_path: str = FileSpec(rel_path).abs_path
    with open(abs_path, "r", encoding="utf-8-sig") as f:
        line: str = f.readline()  # skip header

        while line:
            line = f.readline()
            if line == "":
                break
            fields: list[str] = line.rstrip().split("|")

            block: str = fields[0]
            vtd: str = "".join([fips, fields[1], fields[2]])

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
