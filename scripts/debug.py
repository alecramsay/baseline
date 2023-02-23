#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


### HARDCODE ARGS ###

# fips_map: dict[str, str] = make_state_codes()
xx: str = "MN"
plan_type: str = "congress"
verbose: bool = True


### DEBUG ###

baseline_with_vtds(xx, plan_type, verbose)
# baseline_with_bgs(xx, plan_type, verbose)

### END ###
