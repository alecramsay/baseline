#!/usr/bin/env python3
"""
Run a batch of commands.

For example:

$ scripts/run_batch.py

"""

import os

from baseline import *

# for xx in study_states:
#     if xx in ["NJ", "NC"]:
#         continue  # Already done

#     command: str = f"scripts/unpickle_graph.py -s {xx}"
#     print(command)
#     os.system(command)

for xx in ["CA", "OR", "WV"]:
    command: str = f"scripts/unpickle_graph.py -s {xx}"
    print(command)
    os.system(command)

pass
