#!/usr/bin/env python3

"""
DEBUG
"""

import argparse
from argparse import ArgumentParser, Namespace
from collections import defaultdict

from baseline import *


def main() -> None:
    xx: str = "MI"

    rel_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "water_only"], "_", "csv"
    )  # GEOID,ALAND,AWATER
    types: list = [str, int, int]
    water_precincts: list = [row["GEOID"] for row in read_typed_csv(rel_path, types)]

    pass


if __name__ == "__main__":
    main()

### END ###
