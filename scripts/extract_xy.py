#!/usr/bin/env python3
#

"""
Extract the centroid coordinates of a state's geographic units.

For example:

$ scripts/extract_xy.py -s NC -p

For documentation, type:

$ scripts/extract_xy.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from shapely.geometry import Point

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
        "-t",
        "--tract",
        dest="tract",
        action="store_true",
        help="Generate tract-level data",
    )
    parser.add_argument(
        "-g", "--bg", dest="bg", action="store_true", help="Generate BG-level data"
    )
    parser.add_argument(
        "-p",
        "--precinct",
        dest="precinct",
        action="store_true",
        help="Generate VTD-level data",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


### HELPERS ###


def find_center(shp) -> Coordinate:
    x: float = shp.centroid.x
    y: float = shp.centroid.y

    if not shp.contains(Point(x, y)):
        # Get a centroid-like point guaranteed to be w/in the feature
        pt: Point = shp.representative_point()
        x: float = pt.x
        y: float = pt.y

    return Coordinate(x, y)


def find_centers(feature_shps) -> dict[str, Coordinate]:
    feature_xy: defaultdict[str, Coordinate] = defaultdict()

    for item in feature_shps[0].items():
        geoID: str = item[0]
        shp: Polygon | MultiPolygon = item[1]

        coord: Coordinate = find_center(shp)
        feature_xy[geoID] = coord

    return feature_xy


def main() -> None:
    """Extract x,y coordinates from TIGER/Line shapefiles."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = STATE_FIPS

    xx: str = args.state
    fips: str = fips_map[xx]

    tracts: bool = args.tract
    bgs: bool = args.bg
    blocks: bool = True  # args.block
    vtds: bool = args.precinct

    verbose: bool = args.verbose

    state_dir: str = xx

    ### READ THE SHAPEFILES, EXTRACT THE CENTROIDS, AND PICKLE THEM ###

    # Tracts

    if tracts:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, "tract"], "_"
        )
        tract_shps: tuple[dict, Optional[dict[str, Any]]] = read_shapes(
            rel_path, unit_id("tract")
        )
        feature_xy: dict[str, Coordinate] = find_centers(tract_shps)

        del tract_shps

        rel_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, "tract", "xy"], "_", "pickle"
        )
        write_pickle(rel_path, feature_xy)

        del feature_xy

    # Blockgroups

    if bgs:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, "bg"], "_"
        )
        bg_shps: tuple[dict, Optional[dict[str, Any]]] = read_shapes(
            rel_path, unit_id("bg")
        )
        feature_xy: dict[str, Coordinate] = find_centers(bg_shps)

        del bg_shps

        rel_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, "bg", "xy"], "_", "pickle"
        )
        write_pickle(rel_path, feature_xy)

        del feature_xy

    # Blocks

    if blocks:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, "tabblock20"], "_"
        )
        block_shps: tuple[dict, Optional[dict[str, Any]]] = read_shapes(
            rel_path, unit_id("block")
        )
        feature_xy: dict[str, Coordinate] = find_centers(block_shps)

        del block_shps

        rel_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, "block", "xy"], "_", "pickle"
        )
        write_pickle(rel_path, feature_xy)

        del feature_xy

    # Precincts (VTDs)

    if vtds:
        rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
            ["tl_2020", fips, "vtd20"], "_"
        )
        vtd_shps: tuple[dict, Optional[dict[str, Any]]] = read_shapes(
            rel_path, unit_id("vtd")
        )
        feature_xy: dict[str, Coordinate] = find_centers(vtd_shps)

        del vtd_shps

        rel_path: str = path_to_file([temp_dir]) + file_name(
            [xx, cycle, "vtd", "xy"], "_", "pickle"
        )
        write_pickle(rel_path, feature_xy)

        del feature_xy


if __name__ == "__main__":
    main()

### END ###
