#!/usr/bin/env python3
#
# SAMPLE CODE
#

from collections import defaultdict
from typing import Any

from baseline import *


### ARGS ###

xx: str = "NC"
fips: str = "37"
verbose: bool = True

state_dir: str = xx


### READ THE CENSUS DATA, PIVOT IT, AND WRITE CSVS ###

rel_path: str = path_to_file(
    [rawdata_dir, state_dir]
    + file_name([cycle, "vt_Census_block", fips, "data2"], "_", "json")
)

pop_by_block: defaultdict[str, int] = read_census_json(rel_path)
pop_by_tract: defaultdict[str, int] = defaultdict(int)
pop_by_bg: defaultdict[str, int] = defaultdict(int)

tract_bgs: defaultdict[str, set[str]] = defaultdict(set)
bg_blocks: defaultdict[str, set[str]] = defaultdict(set)

blocks: list[dict] = []
total_pop: int = 0
max_block_pop: int = 0

for block, pop in pop_by_block.items():
    blocks.append({"GEOID": block, "POP": pop})

    g: GeoID = GeoID(block)
    tract: str = g.tract
    bg: str = g.bg

    pop_by_tract[tract] += pop
    pop_by_bg[bg] += pop

    total_pop += pop

    if pop > max_block_pop:
        max_block_pop = pop

    tract_bgs[tract].add(bg)
    bg_blocks[bg].add(block)

pass

#
