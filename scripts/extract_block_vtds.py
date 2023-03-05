#!/usr/bin/env python3
#

"""
Create a dict of blocks and their associated VTDs.

For example:

$ scripts/extract_block_vtds.py -s NC

For documentation, type:

$ scripts/extract_block_vtds.py -h
"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of GEOIDs to friendly names."
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

    fips_map: dict[str, str] = make_state_codes()

    xx: str = args.state
    fips: str = fips_map[xx]

    verbose: bool = args.verbose

    ### READ THE CENSUS FILE & CREATE THE MAPPINGS ###

    unit: str = "bg" if xx in ["CA", "OR"] else "vtd"

    rel_path: str = path_to_file([rawdata_dir, xx]) + file_name(
        ["BlockAssign", f"ST{fips}", xx, unit.upper()], "_", "txt"
    )

    vtd_blocks: dict[str, list[str]] = dict()  # NOTE - Not pickled at this time
    block_vtd: dict[str, str] = dict()

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

            block_vtd[block] = vtd

            if vtd not in vtd_blocks:
                vtd_blocks[vtd] = list()

            vtd_blocks[vtd].append(block)

    pass

    ### PICKLE THE RESULTS ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "block", "vtd"], "_", "pickle"
    )
    write_pickle(rel_path, block_vtd)

    pass


if __name__ == "__main__":
    main()

### END ###
