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
    description="Extract census population data from DRA block data JSON."
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
fips_map: dict[str, str] = make_state_codes()

xx: str = args.state
fips: str = fips_map[xx]
tracts: bool = args.tract
bgs: bool = args.bg
verbose: bool = args.verbose

state_dir: str = xx


### READ THE CENSUS DATA, PIVOT IT BY LEVEL, AND PICKLE IT ###

rel_path: str = path_to_file([rawdata_dir, state_dir]) + file_name(
    [cycle, "vt_Census_block", fips, "data2"], "_", "json"
)

pop_by_block: defaultdict[str, int] = read_census_json(rel_path)
pop_by_tract: defaultdict[str, int] = defaultdict(int)
pop_by_bg: defaultdict[str, int] = defaultdict(int)

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

rel_path: str = path_to_file([temp_dir]) + file_name(
    [xx, cycle, "block", "pop"], "_", "pickle"
)
write_pickle(rel_path, pop_by_block)

nblocks: int = len(pop_by_block)
del pop_by_block


# Tracts

max_tract_pop: int = 0

for tract, pop in pop_by_tract.items():
    if pop > max_tract_pop:
        max_tract_pop = pop

if tracts:
    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "tract", "pop"], "_", "pickle"
    )
    write_pickle(rel_path, pop_by_tract)

ntracts: int = len(pop_by_tract)
del pop_by_tract


# Blockgroups

max_bg_pop: int = 0
for bg, pop in pop_by_bg.items():
    if pop > max_bg_pop:
        max_bg_pop = pop

if bgs:
    rel_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "bg", "pop"], "_", "pickle"
    )
    write_pickle(rel_path, pop_by_bg)

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
