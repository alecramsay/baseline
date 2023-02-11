#!/usr/bin/env python3
#

"""
Generate seeds for district sites, using a plastic sequence.

For example:

$ scripts/generate_seeds.py NC congress -v

For documentation, type:

$ scripts/generate_seeds.py -h


NOTE - To use this script, you must first download the appropriate state shapefiles locally.
"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Generate seeds for district sites."
)

parser.add_argument("state", help="The two-character state code, e.g., NC.", type=str)
parser.add_argument(
    "type", help="The type of map: { congress | upper | lower }.", type=str
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()
fips_map: dict[str, str] = make_state_codes()

xx: str = args.state
fips: str = fips_map[xx]
plan_type: str = args.type
n: int = districts_by_state[xx][plan_type]

verbose: bool = args.verbose


### CONSTRUCT PATHS ###

state_dir: str = xx

state_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
    ["tl", cycle, fips, "state20"], "_"
)


### GENERATE SEEDS ###

state_shp: Polygon | MultiPolygon = load_state_shape(state_path, unit_id("state"))
seeder: PlasticCoordinates = PlasticCoordinates(n, state_shp)
seeder.echo()

#
