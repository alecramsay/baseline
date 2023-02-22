#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/preprocess_state.py -s NC -t congress
$ scripts/preprocess_state.py -s MD -t congress
$ scripts/preprocess_state.py -s PA -t congress
$ scripts/preprocess_state.py -s VA -t congress

For documentation, type:

$ scripts/preprocess_state.py -h

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
        "-t",
        "--type",
        default="congress",
        help="The type of map: { congress | upper | lower }.",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Preprocess data for a state."""

    args: Namespace = parse_args()
    xx: str = args.state
    plan_type: str = args.type

    verbose: bool = args.verbose

    print(f"Preprocessing data for {xx} {plan_type} ...")


if __name__ == "__main__":
    main()

### END ###
