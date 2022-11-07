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
    description="Find population compact districts."
)

parser.add_argument("state", help="The two-character state code (e.g., MD)", type=str)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

cycle: str = "2020"
xx: str = args.state
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

data_dir: str = "data/"
temp_dir: str = "temp/"
state_dir: str = xx + "/"


### JOIN THE POPULATION & COORDINATE DATA BY GEOID ###

for unit in ["tract", "bg", "block"]:
    pop_path: str = temp_dir + file_name(xx, cycle, unit, "pop", "pickle")
    xy_path: str = temp_dir + file_name(xx, cycle, unit, "xy", "pickle")

    pop: bytes | None = read_pickle(pop_path)
    xy: bytes | None = read_pickle(xy_path)

    features: list[Feature] = []

    for geoid, pop in pop.items():
        features.append({"geoid": geoid, "pop": pop, "xy": xy[geoid], "district": 0})

    join_path: str = data_dir + state_dir + file_name(xx, cycle, unit, "data", "pickle")
    write_pickle(join_path, features)
