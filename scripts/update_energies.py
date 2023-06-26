#!/usr/bin/env python3
#

"""
Update the energies for a state.

For example:

$ scripts/update_energies.py -s AZ

For documentation, type:

$ scripts/update_energies.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Update the energies for a state."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="AZ",
        help="The two-character state code (e.g., AZ)",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Update the energies for a state."""

    args: Namespace = parse_args()
    xx: str = args.state
    verbose: bool = args.verbose

    #

    commands: list[str]
    commands = [
        "scripts/log_energies.py -s {xx} -v > intermediate/{xx}/{xx}20C_log_energies.txt",
        "scripts/energies_to_csv.py -s {xx} -v",
    ]

    for command in commands:
        command: str = command.format(xx=xx)
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
