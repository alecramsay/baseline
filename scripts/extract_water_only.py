#!/usr/bin/env python3
#

"""
Extract the water-only VTDs (precincts).

For example:

$ scripts/extract_water_only.py -s NC
$ scripts/extract_water_only.py -s MD > data/MD/MD_2020_water_only.csv

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
    """Find water-only VTDs (precincts)."""

    args: Namespace = parse_args()

    xx: str = args.state
    vtds: bool = True  # Just do VTDs (precincts) for now
    verbose: bool = args.verbose

    ### DEBUG ###

    ### READ THE SHAPEFILES ###

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]
    state_dir: str = xx

    unit: str = "bg" if xx in ["CA", "OR"] else "vtd"
    unit_label: str = "vtd20" if unit == "vtd" else "bg"

    if vtds:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, unit_label], "_"
        )
        id: str = unit_id(unit)

        shp_file: str = os.path.expanduser(rel_path)
        water_only: bool = False

        with fiona.Env():
            with fiona.open(shp_file) as source:
                if source:
                    for item in source:
                        geoid: str = item["properties"][id]
                        land_key: str = "ALAND20" if unit == "vtd" else "ALAND"
                        water_key: str = "AWATER20" if unit == "vtd" else "AWATER"
                        aland: int = item["properties"][land_key]
                        awater: int = item["properties"][water_key]
                        vtd: str = (
                            item["properties"]["VTDST20"]
                            if "VTDST20" in item["properties"]
                            else "N/A"
                        )

                        if (awater > 0 and aland == 0) or vtd == "ZZZZZZ":
                            if not water_only:
                                water_only = True
                                print(f"GEOID,ALAND,AWATER")

                            print(f"{geoid},{aland},{awater}")

        if not water_only:
            print()
            print(f"No water-only VTDs (precincts) for {xx}")
            print()
        else:
            print()

        pass


if __name__ == "__main__":
    main()

### END ###
