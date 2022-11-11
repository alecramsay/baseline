#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/find_base_districts.py NC congress tract -v -n
$ scripts/find_base_districts.py NC congress tract -v > results/NC/NC_2020_congress_tract_log.txt

$ scripts/find_base_districts.py NC congress bg -v > results/NC/NC_2020_congress_bg_log.txt

For documentation, type:

$ scripts/find_base_districts.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Find population compact districts."
)

parser.add_argument("state", help="The two-character state code, e.g., NC.", type=str)
parser.add_argument(
    "type", help="The type of map: { congress | upper | lower }.", type=str
)
parser.add_argument("units", help="The unit of granularity: { tract | bg }.", type=str)

parser.add_argument(
    "-n", "--noplan", dest="noplan", action="store_true", help="No plan mode"
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
units: str = args.units

noplan: bool = args.noplan
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

data_dir: str = "data" + "/"
results_dir: str = "results" + "/"
state_dir: str = xx + "/"

features_path: str = (
    data_dir + state_dir + file_name([xx, cycle, units, "data"], "_", "pickle")
)
state_path: str = data_dir + state_dir + file_name(["tl", cycle, fips, "state20"], "_")
plan_path: str = (
    results_dir + state_dir + file_name([xx, cycle, plan_type, units], "_", "csv")
)


### FIND DISTRICTS ###

features: list[Feature] = read_pickle(features_path)
state_shp: Polygon | MultiPolygon = load_state_shape(state_path, "GEOID20")
seeds: list[Coordinate] = PlasticCoordinates(n, state_shp).generate()

# TODO -- Integrate Todd's Balzer district solver here.
# solver: DistrictSolver = DistrictSolver(settings, args.verbose)
# success: bool = solver.minimize_district_moi()
plan: list[Assignment] = None
#

if plan:
    print("Success!")
    if not noplan:
        write_csv(plan_path, plan)

#
