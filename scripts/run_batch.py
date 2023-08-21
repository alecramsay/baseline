#!/usr/bin/env python3
#
# SAMPLE CODE
#

import os

from baseline import *

run_states: list[str] = ["NC", "VA", "CO"]
fail_states: list[str] = ["MD", "AZ", "GA"]
bg_states: list[str] = ["CA", "OR", "WV"]
exclude: list[str] = run_states + fail_states + bg_states

states: list[str] = [xx for xx in study_states if xx not in exclude]
print(states)
print(len(states))

for xx in states:
    command: str = f"scripts/extract_blocks_by_vtd.py -s {xx}"
    # print(command)
    os.system(command)

pass
