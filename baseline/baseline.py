#!/usr/bin/env python3

"""
BASELINE DISTRICTS
"""

import os

from .constants import *
from .utils import *
from .readwrite import *


def do_baseline_run(
    tmpdir: str,
    N: int,
    seed: int,
    prefix: str,
    data: str,
    adjacencies: str,
    output: str,
    label: str,
    verbose: bool = False,
) -> None:
    """Make a set of baseline districts from random starting sites

    Do this many times, and then choose the baseline as the map with the lowest energy.
    """

    command: str = f"create.sh --tmpdir={tmpdir} --N={N} --seed={seed} --prefix={prefix} --data={data} --adjacencies={adjacencies} --output={output} --label={label}"
    os.system(command)


### HELPER FUNCTIONS ###


def full_path(dirs: list[str], file_parts: list[str], ext: str = "csv") -> str:
    """Return a fully qualifed file name from a list of directories and a list of file parts"""

    rel_path: str = path_to_file(dirs) + file_name(file_parts, "_", ext)
    return FileSpec(rel_path).abs_path


def label_map(xx: str, plan_type: str) -> str:
    return f"{xx}{cycle[2:]}{plan_type.upper()[0]}"


def label_iteration(I: int, K: int, N: int) -> str:
    return f"I{I:03d}K{K:02d}N{N:02d}"


### END ###
