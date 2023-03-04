#!/usr/bin/env python3
#

"""
Extract the water-only precincts.

For example:

$ scripts/extract_water_only.py -s NC

For documentation, type:

$ scripts/extract_water_only.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from shapely.geometry import shape, Polygon, MultiPolygon
import fiona

from baseline import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract x,y coordinates from TIGER/Line shapefiles."
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
    """Find water-only precincts."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = make_state_codes()

    xx: str = args.state
    fips: str = fips_map[xx]

    precincts: bool = True  # Just do precincts for now

    verbose: bool = args.verbose

    state_dir: str = xx

    ### READ THE SHAPEFILES ###

    unit: str = "bg" if xx in ["CA", "OR"] else "vtd"
    unit_label: str = "vtd20" if unit == "vtd" else "bg"

    if precincts:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, unit_label], "_"
        )
        id: str = unit_id(unit)

        shp_file: str = os.path.expanduser(rel_path)
        water_only: bool = False

        with fiona.Env():
            with fiona.open(shp_file) as source:
                meta: dict[str, Any] = source.meta
                for item in source:
                    geoid: str = item["properties"][id]
                    land_key: str = "ALAND20" if unit == "vtd" else "ALAND"
                    water_key: str = "AWATER20" if unit == "vtd" else "AWATER"
                    aland: int = item["properties"][land_key]
                    awater: int = item["properties"][water_key]

                    if awater > 0 and aland == 0:
                        if not water_only:
                            water_only = True

                            print()
                            print(f"Water-only precincts for {xx}:")
                            print()

                        print(f"GEOID,ALAND,AWATER")
                        print(f"{geoid},{aland},{awater}")

        if not water_only:
            print()
            print(f"No water-only precincts for {xx}")
            print()
        else:
            print()

        pass  # TODO


if __name__ == "__main__":
    main()

### END ###
