#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py NC congress -v > results/NC/NC_2020_congress_log.txt

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

bg_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "bg", "data"], "_", "csv"
)
block_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "block", "data"], "_", "csv"
)
plan_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, plan_type], "_", "csv"
)

abs_path: str = FileSpec(bg_path).abs_path
with open(abs_path, "r", encoding="utf-8-sig") as file:
    print("BG CSV opened")

abs_path: str = FileSpec(block_path).abs_path
with open(abs_path, "r", encoding="utf-8-sig") as file:
    print("Block CSV opened")

### FIND BASLINE DISTRICTS ###

# TODO -- Integrate Todd's Balzer district solver here.
# solver: DistrictSolver = DistrictSolver(settings, args.verbose)
# success: bool = solver.minimize_district_moi()
# plan: list[Assignment] = None
# #

# if plan:
#     print("Success!")
#     if not noplan:
#         write_csv(plan_path, plan)

#
