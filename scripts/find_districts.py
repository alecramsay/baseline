#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/find_districts.py "data/NC/NC_congress.json" -v -n

$ scripts/find_districts.py "data/AZ/AZ_congress.json" -v > results/AZ/AZ_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/MD/MD_congress.json" -v > results/MD/MD_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/NC/NC_congress.json" -v > results/NC/NC_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/NY/NY_congress.json" -v > results/NY/NY_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/PA/PA_congress.json" -v > results/PA/PA_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/TX/TX_congress.json" -v > results/TX/TX_2020_congress_tract_log.txt
$ scripts/find_districts.py "data/VA/VA_congress.json" -v > results/VA/VA_2020_congress_tract_log.txt

$ scripts/find_districts.py "data/NY/NY_congress.json" -v > results/NY/NY_2020_congress_bg_log.txt
$ scripts/find_districts.py "data/PA/PA_congress.json" -v > results/PA/PA_2020_congress_bg_log.txt
$ scripts/find_districts.py "data/VA/VA_congress.json" -v > results/VA/VA_2020_congress_bg_log.txt
$ scripts/find_districts.py "data/TX/TX_congress.json" -v > results/TX/TX_2020_congress_bg_log.txt

$ scripts/find_districts.py "data/NC/NC_congress.json" -v > results/NC/NC_2020_congress_bg_log.txt

For documentation, type:

$ scripts/find_districts.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from typing import Any

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Find population compact districts."
)

parser.add_argument(
    "config", help="The relative path to a solver settings JSON file", type=str
)
parser.add_argument(
    "-n", "--noplan", dest="noplan", action="store_true", help="No plan mode"
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

settings: dict[str, Any] = load_json(args.config)

xx: str = settings["state"]
cycle: str = settings["cycle"]
fips: str = settings["fips"]
plan_type: str = settings["plan_type"]
units: str = settings["units"]


### CONSTRUCT PATHS ###

data_dir: str = "data" + "/"
results_dir: str = "results" + "/"
state_dir: str = xx + "/"

tract_features: str = (
    data_dir + state_dir + file_name([xx, cycle, "tract", "data"], "_", "pickle")
)
bg_features: str = (
    data_dir + state_dir + file_name([xx, cycle, "bg", "data"], "_", "pickle")
)
state_feature: str = (
    data_dir + state_dir + file_name(["tl", cycle, fips, "state20"], "_")
)
plan_path: str = (
    results_dir + state_dir + file_name([xx, cycle, plan_type, units], "_", "csv")
)

settings["features_paths"] = [tract_features, bg_features]
settings["state_path"] = state_feature
settings["plan_path"] = plan_path


### FIND DISTRICTS ###

solver: DistrictSolver = DistrictSolver(settings, args.verbose)
success: bool = solver.minimize_district_moi()

if success:
    print()
    print("Success!")
    if not args.noplan:
        solver.write_plan()
