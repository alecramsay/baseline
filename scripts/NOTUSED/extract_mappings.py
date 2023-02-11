#!/usr/bin/env python3
#

"""
Extract track and blockgroup (BG) mappings to blocks.

For example:

$ scripts/extract_mappings.py MD
$ scripts/extract_mappings.py NC
$ scripts/extract_mappings.py PA
$ scripts/extract_mappings.py VA
$ scripts/extract_mappings.py NY

For documentation, type:

$ scripts/extract_mappings.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict

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
fips_map: dict[str, str] = make_state_codes()

xx: str = args.state
fips: str = fips_map[xx]
verbose: bool = args.verbose

state_dir: str = xx


### READ THE CENSUS DATA FOR THE BLOCK GEOIDS ###

rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
    [f"{cycle}vt_Census_block", fips, "data2"], "_", "json"
)
pop_by_block: defaultdict[str, int] = read_census_json(rel_path)


### 'PIVOT' THE BLOCKS INTO TRACTS AND BGS ###

tract_bgs: defaultdict[str, set[str]] = defaultdict(set)
bg_blocks: defaultdict[str, set[str]] = defaultdict(set)

total_pop: int = 0
max_block_pop: int = 0

for block, _ in pop_by_block.items():
    g: GeoID = GeoID(block)
    tract: str = g.tract
    bg: str = g.bg

    tract_bgs[tract].add(bg)
    bg_blocks[bg].add(block)

rel_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "tract", "map"], "_", "pickle"
)
write_pickle(rel_path, tract_bgs)

rel_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "bg", "map"], "_", "pickle"
)
write_pickle(rel_path, bg_blocks)

#
