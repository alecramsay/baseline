#!/usr/bin/env python3
#

"""
Find districts that minimize population compactness (moment of inertia).

For example:

$ scripts/baseline_state.py NC congress -v > maps/NC20C_vtd_log.txt
$ scripts/baseline_state.py MD congress -v > maps/MD20C_vtd_log.txt
$ scripts/baseline_state.py PA congress -v > maps/PA20C_vtd_log.txt
$ scripts/baseline_state.py VA congress -v > maps/VA20C_vtd_log.txt

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
    "-g", "--bg", dest="bg", action="store_true", help="Generate BG-level data"
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

xx: str = args.state
plan_type: str = args.type
bg: bool = args.bg

verbose: bool = args.verbose

if bg:
    baseline_with_bgs(xx, plan_type, verbose)
else:
    baseline_with_vtds(xx, plan_type, verbose)

### END ###
