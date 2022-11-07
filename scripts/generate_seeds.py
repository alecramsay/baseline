#!/usr/bin/env python3
#

"""
Generate seeds for district sites, using a plastic sequence.

For example:

$ scripts/generate_seeds.py NC congress -v

For documentation, type:

$ scripts/generate_seeds.py -h

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
cycle: str = "2020"
fips: str = fips_map[xx]
plan_type: str = args.type
n: int = districts_by_state[xx][plan_type]

verbose: bool = args.verbose


### CONSTRUCT PATHS ###

data_dir: str = "data" + "/"
results_dir: str = "results" + "/"
state_dir: str = xx + "/"

state_path: str = data_dir + state_dir + file_name("tl", cycle, fips, "state20")


### GENERATE SEEDS ###

state_shp: Polygon | MultiPolygon = load_state_shape(state_path, "GEOID20")
seeder: PlasticCoordinates = PlasticCoordinates(n, state_shp)
seeder.echo()

#
