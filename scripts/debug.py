#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


### HARDCODE ARGS ###

fips_map: dict[str, str] = make_state_codes()
xx: str = "NC"
fips: str = fips_map[xx]
plan_type: str = "congress"
n: int = districts_by_state[xx][plan_type]

verbose: bool = True


### CONSTRUCT PATHS ###

state_dir: str = xx

bg_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "bg", "data"], "_", "csv"
)
block_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, "block", "data"], "_", "csv"
)
plan_path: str = path_to_file([data_dir, state_dir]) + file_name(
    [xx, cycle, plan_type], "_", "csv"
)

# abs_path: str = FileSpec(bg_path).abs_path
# with open(abs_path, "r", encoding="utf-8-sig") as file:
#     print("BG CSV opened")

# abs_path: str = FileSpec(block_path).abs_path
# with open(abs_path, "r", encoding="utf-8-sig") as file:
#     print("Block CSV opened")


### FIND BASLINE DISTRICTS ###

# TODO -- Integrate Todd's Balzer district solver here.
# solver: DistrictSolver = DistrictSolver(settings, args.verbose)
# success: bool = solver.minimize_district_moi()
# plan: list[Assignment] = None
# #

# if plan:
#     print("Success!")
#     if not noplan:
#         write_csv(plan_path, plan)

### END ###
