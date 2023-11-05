#!/usr/bin/env python3
"""
Run a batch of commands.

For example:

$ scripts/run_batch.py

"""

import os

from baseline import *

for xx in ["CA", "OR", "WV"]:
    name: str = f"{xx}_2020_{study_unit(xx)}_graph.json"
    command: str = f"cp data/{xx}/{name} ../rdafn/data/{xx}/{name}"
    print(command)
    os.system(command)


pass
