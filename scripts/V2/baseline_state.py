#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py -s NC -v > logs/NC_2020_congress_log.txt
$ scripts/baseline_state.py -s MD -v > logs/MD_2020_congress_log.txt
$ scripts/baseline_state.py -s PA -v > logs/PA_2020_congress_log.txt
$ scripts/baseline_state.py -s VA -v > logs/VA_2020_congress_log.txt

$ scripts/baseline_state.py -s MN -v > logs/MN_2020_congress_log.txt
$ scripts/baseline_state.py -s NV -v > logs/NV_2020_congress_log.txt
$ scripts/baseline_state.py -s NM -v > logs/NM_2020_congress_log.txt
$ scripts/baseline_state.py -s NY -v > logs/NY_2020_congress_log.txt
$ scripts/baseline_state.py -s TN -v > logs/TN_2020_congress_log.txt
$ scripts/baseline_state.py -s WA -v > logs/WA_2020_congress_log.txt

$ scripts/baseline_state.py -s OR -g -v > logs/OR_2020_congress_log.txt
$ scripts/baseline_state.py -s CA -t -v > logs/CA_2020_congress_log.txt

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

parser.add_argument(
    "-s",
    "--state",
    default="NC",
    help="The two-character state code (e.g., NC)",
    type=str,
)
parser.add_argument(
    "-m",
    "--map",
    default="congress",
    help="The type of map: { congress | upper | lower }.",
    type=str,
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
plan_type: str = args.map
bg: bool = args.bg
tract: bool = args.tract

verbose: bool = args.verbose

if bg:
    baseline_state_WIP(xx, plan_type, "bg", "bg", verbose)
elif tract:  # CA
    baseline_state_WIP(xx, plan_type, "tract", "bg", verbose)
else:
    baseline_state_WIP(xx, plan_type, "vtd", "vtd", verbose)

### END ###
