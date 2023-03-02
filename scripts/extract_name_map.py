#!/usr/bin/env python3
#

"""
Create a mapping of GEOIDs to friendly names.

For example:

$ scripts/extract_name_map.py -s NC > data/NC/NC_NAMES.txt

For documentation, type:

$ scripts/extract_name_map.py -h

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
    """Create a mapping of GEOIDs to friendly names."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = make_state_codes()

    xx: str = args.state
    fips: str = fips_map[xx]

    verbose: bool = args.verbose

    state_dir: str = xx

    ### READ THE SHAPEFILES ###

    unit: str = "bg" if xx in ["CA", "OR"] else "vtd"

    rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
        ["NAMES", f"ST{fips}", xx, unit.upper()], "_", "txt"
    )
    id: str = unit_id(unit)

    abs_path: str = FileSpec(rel_path).abs_path
    with open(abs_path, "r", encoding="utf-8-sig") as f:
        line: str = f.readline()  # skip header

        print()
        print(f"GEOID,NAME")
        while line:
            line = f.readline()
            if line == "":
                break
            fields: list[str] = line.split("|")
            geoid: str = "".join([fields[0], fields[1], fields[2]])
            name: str = fields[3]
            print(f"{geoid},{name}")

    pass  # TODO


if __name__ == "__main__":
    main()

### END ###