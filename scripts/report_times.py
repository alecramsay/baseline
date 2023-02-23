#!/usr/bin/env python3

"""
Report run times by state
"""

from baseline import *

print(f"XX,N,SECONDS")
for xx in study_states:
    n: int = districts_by_state[xx]["congress"]

    rel_path: str = path_to_file(["logs"]) + file_name(
        [xx, f"{cycle}", "congress", "log"], "_", "txt"
    )

    abs_path: str = FileSpec(rel_path).abs_path
    with open(abs_path, "r", encoding="utf-8-sig") as f:
        line: str = f.readline()
        while line:
            if line.startswith("baseline_state ="):
                seconds: float = float(line.split()[2])
                break
            line = f.readline()

        print(f"{xx},{n},{seconds}")


### END ###
