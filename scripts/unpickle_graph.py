#!/usr/bin/env python3
"""
Unpickle a graph and write it back out as a JSON file.

For example:

$ scripts/unpickle_graph.py -s NC

For documentation, type:

$ scripts/unpickle_graph.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Unpickle a graph and write it back out as a JSON file."
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
    """Unpickle a graph and write it back out as a JSON file."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    #

    ### LOAD DATA ###

    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "vtd", "graph"], "_", "pickle"
    )
    g: dict = read_pickle(rel_path)

    ### WRITE DATA AS A JSON FILE ###

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "vtd", "graph"], "_", "json"
    )
    write_json(rel_path, g)


if __name__ == "__main__":
    main()

### END ###
