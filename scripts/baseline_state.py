#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py NC congress -v > logs/NC_2020_congress_log.txt
$ scripts/baseline_state.py MD congress -v > logs/MD_2020_congress_log.txt
$ scripts/baseline_state.py PA congress -v > logs/PA_2020_congress_log.txt
$ scripts/baseline_state.py VA congress -v > logs/VA_2020_congress_log.txt

$ scripts/baseline_state.py OR congress -g -v > logs/OR_2020_congress_log.txt
$ scripts/baseline_state.py CA congress -t -v > logs/CA_2020_congress_log.txt

For documentation, type:

$ scripts/baseline_state.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any

from baseline import *

parser: ArgumentParser = argparse.ArgumentParser(
    description="Find population compact districts."
)

parser.add_argument("state", help="The two-character state code, e.g., NC.", type=str)
parser.add_argument(
    "type", help="The type of map: { congress | upper | lower }.", type=str
)
parser.add_argument(
    "-g",
    "--bg",
    dest="bg",
    action="store_true",
    help="Use block groups instead of VTDs.",
)
parser.add_argument(
    "-t",
    "--tract",
    dest="tract",
    action="store_true",
    help="Use tracts to iterate, BGs to finish.",
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

xx: str = args.state
plan_type: str = args.type
bg: bool = args.bg
tract: bool = args.tract

verbose: bool = args.verbose

if bg:
    baseline_state(xx, plan_type, "bg", "bg", verbose)
elif tract:  # CA
    baseline_state(xx, plan_type, "tract", "bg", verbose)
else:
    baseline_state(xx, plan_type, "vtd", "vtd", verbose)

### END ###
