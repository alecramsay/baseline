#!/usr/bin/env python3
#

"""
Expand a precinct-assignment file into a block-assignment file

For example:

$ scripts/expand_vtds_to_blocks.py -s NC

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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Expand a precinct-assignment file into a block-assignment file."""

    args: Namespace = parse_args()

    xx: str = args.state
    plan_type: str = "congress"
    verbose: bool = args.verbose

    # Constants

    map_label: str = label_map(xx, plan_type)

    # Unpickle blocks by vtd

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "vtd", "blocks"], "_", "pickle"
    )
    blocks_by_vtd: dict = read_pickle(rel_path)

    # Read the precinct-assignment file

    # TODO - Parameterize this
    input: str = os.path.expanduser("~/Downloads")
    input_root: str = FileSpec(input).abs_path
    input_dir: str = os.path.join(input_root, xx) + "/"

    # TODO - Parameterize this
    rel_path: str = input_dir + file_name([map_label, "baseline", "100"], "_", "csv")
    #

    types: list = [str, int]
    vtd_assignments: list = read_csv(rel_path, types)  # A list of dicts

    # Map vtd assignments to block assignments

    block_assignments: list = list()
    for vtd_assignment in vtd_assignments:
        vtd: str = vtd_assignment["GEOID"]
        district: int = vtd_assignment["DISTRICT"]

        for block in blocks_by_vtd[vtd]:
            block_assignments.append({"GEOID": block, "DISTRICT": district})

    # TODO - Parameterize this
    label: str = "Baseline"

    output_dir: str = input_dir
    rel_path: str = output_dir + file_name([xx, yyyy, plan_type, label], "_", "csv")
    write_csv(rel_path, block_assignments, ["GEOID", "DISTRICT"])

    pass


if __name__ == "__main__":
    main()

### END ###
