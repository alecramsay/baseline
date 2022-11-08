#!/usr/bin/env python3
#

"""
Join feature population and xy data by geoid in a list of dicts.

For example:

$ scripts/join_feature_data.py MD
$ scripts/join_feature_data.py NC
$ scripts/join_feature_data.py PA
$ scripts/join_feature_data.py VA
$ scripts/join_feature_data.py NY

For documentation, type:

$ scripts/join_feature_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Join feature population and xy data by geoid."
)

parser.add_argument("state", help="The two-character state code (e.g., MD)", type=str)
parser.add_argument(
    "-t", "--tract", dest="tract", action="store_true", help="Generate tract-level data"
)
parser.add_argument(
    "-g", "--bg", dest="bg", action="store_true", help="Generate BG-level data"
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

cycle: str = "2020"
xx: str = args.state
tracts: bool = args.tract
bgs: bool = args.bg
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

data_dir: str = "data/"
temp_dir: str = "temp/"
state_dir: str = xx + "/"


### JOIN THE POPULATION & COORDINATE DATA BY GEOID ###

units: list[str] = ["block"]
if tracts:
    units.append("tract")
if bgs:
    units.append("bg")

for unit in units:
    pop_path: str = temp_dir + file_name(xx, cycle, unit, "pop", "pickle")
    xy_path: str = temp_dir + file_name(xx, cycle, unit, "xy", "pickle")

    pop: bytes | None = read_pickle(pop_path)
    xy: bytes | None = read_pickle(xy_path)

    features: list[Feature] = []

    for geoid, pop in pop.items():
        features.append({"geoid": geoid, "pop": pop, "xy": xy[geoid], "district": 0})

    join_path: str = data_dir + state_dir + file_name(xx, cycle, unit, "data", "pickle")
    write_pickle(join_path, features)
