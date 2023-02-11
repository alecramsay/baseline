#!/usr/bin/env python3
#
# CONVERT PICKLED DATA TO CSV
#

"""
Convert pickled data to CSV format.

For example:

$ scripts/unpickle_to_csv.py NC tract -v

For documentation, type:

$ scripts/unpickle_to_csv.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict
from typing import Any

from baseline import *


### PARSE ARGS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Unpickle data to CSV format."
)

parser.add_argument("state", help="The two-character state code (e.g., MD)", type=str)
parser.add_argument("units", help="The unit of granularity (e.g., bg)", type=str)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

xx: str = args.state
units: str = args.units

state_dir: str = xx


### LOAD DATA ###

rel_path: str = path_to_file([temp_dir]) + file_name(
    [xx, cycle, units, "data"], "_", "pickle"
)
collection: FeatureCollection = FeatureCollection(rel_path)


### WRITE DATA AS A CSV ###

l: list = list()
for f in collection.features:
    row: dict[str, int, int, int] = {
        "GEOID": f["geoid"],
        "POP": f["pop"],
        "X": f["xy"].x,
        "Y": f["xy"].y,
    }
    l.append(row)


rel_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, units, "data"], "_", "csv"
)
write_csv(rel_path, l, ["GEOID", "POP", "X", "Y"], "{:.14f}")

pass

#
