#!/usr/bin/env python3
#
# SAMPLE CODE
#

from collections import defaultdict
from typing import Any

from baseline import *


### ARGS ###

cycle: str = "2020"
xx: str = "NC"
fips: str = "37"
verbose: bool = True


### CONSTRUCT PATHS ###

root_dir: str = "../../work/DRA2020/analytics/baseline/data/"
block_data: str = cycle + "vt_Census_block_" + fips + "_data2.json"
state_dir: str = xx + "/"


def pop_file_name(geo: str) -> str:
    return xx + "_" + cycle + "_pop_" + geo + ".csv"


### READ THE CENSUS DATA, PIVOT IT, AND WRITE CSVS ###

rel_path: str = root_dir + state_dir + block_data

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
