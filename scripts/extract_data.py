#!/usr/bin/env python3
#

"""
Extract data for a state.

For example:

$ scripts/extract_data.py -s NC
$ scripts/extract_data.py -s MI -w

For documentation, type:

$ scripts/extract_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Preprocess data for a state."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-w", "--water", dest="water", action="store_true", help="Water-only precincts"
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Preprocess VTD (precinct) data for a state."""

    args: Namespace = parse_args()
    xx: str = args.state
    water: bool = args.water

    verbose: bool = args.verbose

    water_flag: str = "-w" if water else ""

    commands: list[str] = [
        "scripts/extract_pop.py -s {xx} -p -i 3 > data/{xx}/{xx}_census_log.txt",
        "scripts/extract_xy.py -s {xx} -p",
        "scripts/join_feature_data.py -s {xx} -p",
        "scripts/unpickle_to_csv.py -s {xx} -u vtd {w}",
        "scripts/unpickle_to_csv.py -s {xx} -u block",
        "scripts/index_geoids.py -s {xx}",
        "scripts/extract_block_vtds.py -s {xx}",
        "scripts/extract_name_map.py -s {xx} > data/{xx}/{xx}_2020_vtd_names.txt",
    ]
    for command in commands:
        command: str = command.format(xx=xx, w=water_flag)
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
