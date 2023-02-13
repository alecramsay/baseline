#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


### HARDCODE ARGS ###

# fips_map: dict[str, str] = make_state_codes()
xx: str = "NC"
# fips: str = fips_map[xx]
plan_type: str = "congress"
# n: int = districts_by_state[xx][plan_type]
verbose: bool = True


### DEBUG ###

baseline_state(xx, plan_type, verbose)

### END ###
