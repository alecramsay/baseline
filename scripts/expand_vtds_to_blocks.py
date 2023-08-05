#!/usr/bin/env python3
#

"""
Expand a precinct-assignment file into a block-assignment file

For example:

$ scripts/expand_vtds_to_blocks.py -s NC -d ~/Downloads/ -f NC20C_baseline_100.csv

For documentation, type:

$ scripts/expand_vtds_to_blocks.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Expand a precinct-assignment file to a block-assignment file."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--iodir",
        default="~/Downloads/",
        help="Path to input/output directory",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--file",
        default="NC20C_baseline_100.csv",
        help="Precinct-assignment file to expand",
        type=str,
    )
    parser.add_argument(
        "-l",
        "--label",
        default="Baseline",
        help="The type of map (e.g., Baseline)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Expand a precinct-assignment file into a block-assignment file."""

    args: Namespace = parse_args()

    xx: str = args.state
    iodir: str = os.path.expanduser(args.iodir)
    paf: str = args.file
    label: str = args.label

    verbose: bool = args.verbose

    # Unpickle blocks by vtd

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "vtd", "blocks"], "_", "pickle"
    )
    blocks_by_vtd: dict = read_pickle(rel_path)

    # Read the precinct-assignment file

    io_root: str = FileSpec(iodir).abs_path
    io_dir: str = os.path.join(io_root, xx) + "/"

    rel_path: str = io_dir + paf

    types: list = [str, int]
    vtd_assignments: list = read_csv(rel_path, types)  # A list of dicts

    # Map vtd assignments to block assignments

    block_assignments: list = list()
    for vtd_assignment in vtd_assignments:
        vtd: str = vtd_assignment["GEOID"]
        district: int = vtd_assignment["DISTRICT"]

        for block in blocks_by_vtd[vtd]:
            block_assignments.append({"GEOID": block, "DISTRICT": district})

    rel_path: str = io_dir + file_name([xx, yyyy, "Congress", label], "_", "csv")
    write_csv(rel_path, block_assignments, ["GEOID", "DISTRICT"])

    pass


if __name__ == "__main__":
    main()

### END ###
