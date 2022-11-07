#!/usr/bin/env python3
#

"""
Extract census total population from DRA block data JSON &
aggregate it by track and blockgroup (BG).

For example:

$ scripts/extract_pop.py MD
$ scripts/extract_pop.py NC
$ scripts/extract_pop.py PA
$ scripts/extract_pop.py VA
$ scripts/extract_pop.py NY

$ scripts/extract_pop.py NC > data/NC/NC_census_log.txt

For documentation, type:

$ scripts/extract_pop.py -h

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
cycle: str = "2020"
fips: str = fips_map[xx]
verbose: bool = args.verbose


### CONSTRUCT PATHS ###

root_dir: str = "../../work/Political Geography/baseline/data/"
block_data: str = cycle + "vt_Census_block_" + fips + "_data2.json"
data_dir: str = "data/"
state_dir: str = xx + "/"
temp_dir: str = "temp/"


### READ THE CENSUS DATA, PIVOT IT BY LEVEL, AND PICKLE IT ###

rel_path: str = root_dir + state_dir + block_data

pop_by_block: defaultdict[str, int] = read_census_json(rel_path)
pop_by_tract: defaultdict[str, int] = defaultdict(int)
pop_by_bg: defaultdict[str, int] = defaultdict(int)

# Tract & BG to block mapping files
# tract_bgs: defaultdict[str, set[str]] = defaultdict(set)
# bg_blocks: defaultdict[str, set[str]] = defaultdict(set)

total_pop: int = 0
max_block_pop: int = 0

for block, pop in pop_by_block.items():
    g: GeoID = GeoID(block)
    tract: str = g.tract
    bg: str = g.bg

    pop_by_tract[tract] += pop
    pop_by_bg[bg] += pop

    total_pop += pop

    if pop > max_block_pop:
        max_block_pop = pop

    # tract_bgs[tract].add(bg)
    # bg_blocks[bg].add(block)

rel_path: str = temp_dir + file_name(xx, cycle, "block", "pop", "pickle")
write_pickle(rel_path, pop_by_block)

nblocks: int = len(pop_by_block)
del pop_by_block


# Tracts

max_tract_pop: int = 0

for tract, pop in pop_by_tract.items():
    if pop > max_tract_pop:
        max_tract_pop = pop

rel_path: str = temp_dir + file_name(xx, cycle, "tract", "pop", "pickle")
write_pickle(rel_path, pop_by_tract)

# rel_path: str = data_dir + state_dir + file_name(xx, cycle, "tract", "map", "pickle")
# write_pickle(rel_path, tract_bgs)

ntracts: int = len(pop_by_tract)
del pop_by_tract


# Blockgroups

max_bg_pop: int = 0
for bg, pop in pop_by_bg.items():
    if pop > max_bg_pop:
        max_bg_pop = pop

rel_path: str = temp_dir + file_name(xx, cycle, "bg", "pop", "pickle")
write_pickle(rel_path, pop_by_bg)

# rel_path: str = data_dir + state_dir + file_name(xx, cycle, "bg", "map", "pickle")
# write_pickle(rel_path, bg_blocks)

nbgs: int = len(pop_by_bg)
del pop_by_bg


### PRINT STATISTICS ###

print()
print("Total population: {:,}".format(total_pop))
print(
    "Max tract population: {:,}".format(max_tract_pop),
    "# of tracts: {:,}".format(ntracts),
)
print(
    "Max BG population: {:,}".format(max_bg_pop),
    "# of BGs: {:,}".format(nbgs),
)
print(
    "Max block population: {:,}".format(max_block_pop),
    "# of blocks: {:,}".format(nblocks),
)
print()
