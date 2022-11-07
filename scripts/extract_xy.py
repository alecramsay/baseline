#!/usr/bin/env python3
#

"""
Extract the centroid coordinates of a state's tracts, blockgroups, and blocks.

For example:

$ scripts/extract_xy.py MD
$ scripts/extract_xy.py NC
$ scripts/extract_xy.py PA
$ scripts/extract_xy.py VA
$ scripts/extract_xy.py NY

For documentation, type:

$ scripts/extract_xy.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Find population compact districts."
)

parser.add_argument("state", help="The two-character state code (e.g., MD)", type=str)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()
fips_map: dict[str, str] = make_state_codes()

xx: str = args.state
cycle: str = "2020"
fips: str = fips_map[xx]
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

root_dir: str = "../../work/Political Geography/baseline/data/"

tract_shps: str = "tl_2020_" + fips + "_tract"
bg_shps: str = "tl_2020_" + fips + "_bg"
block_shps: str = "tl_2020_" + fips + "_tabblock20"

# data_dir: str = "data/"
state_dir: str = xx + "/"
temp_dir: str = "temp/"


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
    feature_xy: defaultdict[str, Coordinate] = defaultdict(Coordinate)

    for item in feature_shps[0].items():
        geoID: str = item[0]
        shp: Polygon | MultiPolygon = item[1]

        coord: Coordinate = find_center(shp)
        feature_xy[geoID] = coord

    return feature_xy


### READ THE SHAPEFILES, EXTRACT THE CENTROIDS, AND PICKLE THEM ###

tract_id: str = "GEOID"
bg_id: str = "GEOID"
block_id: str = "GEOID20"

# Tracts

rel_path: str = root_dir + state_dir + tract_shps
feature_shps: tuple[dict, dict[str, Any]] = load_shapes(rel_path, tract_id)
feature_xy: dict[str, Coordinate] = find_centers(feature_shps)

del feature_shps

rel_path: str = temp_dir + file_name(xx, cycle, "tract", "xy", "pickle")
write_pickle(rel_path, feature_xy)

del feature_xy

# Blockgroups

rel_path: str = root_dir + state_dir + bg_shps
feature_shps: tuple[dict, dict[str, Any]] = load_shapes(rel_path, bg_id)
feature_xy: dict[str, Coordinate] = find_centers(feature_shps)

del feature_shps

rel_path: str = temp_dir + file_name(xx, cycle, "bg", "xy", "pickle")
write_pickle(rel_path, feature_xy)

del feature_xy

# Blocks

rel_path: str = root_dir + state_dir + block_shps
feature_shps: tuple[dict, dict[str, Any]] = load_shapes(rel_path, block_id)
feature_xy: dict[str, Coordinate] = find_centers(feature_shps)

del feature_shps

rel_path: str = temp_dir + file_name(xx, cycle, "block", "xy", "pickle")
write_pickle(rel_path, feature_xy)

del feature_xy
