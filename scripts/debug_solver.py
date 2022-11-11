#!/usr/bin/env python3
#
# SAMPLE CODE
#

import json
from collections import defaultdict
from typing import Any

from baseline import *


### ARGS ###

settings_path: str = "data/NC/NC_congress.json"
settings: dict[str, Any] = load_json(settings_path)

xx: str = settings["state"]
cycle: str = settings["cycle"]
fips: str = settings["fips"]
plan_type: str = settings["plan_type"]
units: str = settings["units"]

verbose: bool = True


### CONSTRUCT PATHS ###

data_dir: str = "data" + "/"
results_dir: str = "results" + "/"
state_dir: str = xx + "/"

tract_features: str = (
    data_dir + state_dir + file_name([xx, cycle, "tract", "data"], "_", "pickle")
)
bg_features: str = (
    data_dir + state_dir + file_name([xx, cycle, "bg", "data"], "_", "pickle")
)
# tract_graph: str = (
#     data_dir + state_dir + file_name([xx, cycle, "tract", "graph"], "_", "pickle")
# )
# bg_graph: str = data_dir + state_dir + file_name([xx, cycle, "bg", "graph"], "_", "pickle")
state_feature: str = (
    data_dir + state_dir + file_name(["tl", cycle, fips, "state20"], "_")
)
plan_path: str = (
    results_dir + state_dir + file_name([xx, cycle, plan_type, units], "_", "csv")
)

settings["features_paths"] = [tract_features, bg_features]
settings["state_path"] = state_feature
settings["plan_path"] = plan_path


### FIND DISTRICTS ###

solver: DistrictSolver = DistrictSolver(settings, verbose)
solver.minimize_district_moi()

# solver.write_plan()

pass
