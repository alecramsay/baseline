#!/usr/bin/env python3
#
# HELPERS
#

import time
from functools import wraps
from typing import Any, Callable


def population_deviation(populations: list[int], mean: int) -> float:
    """
    Compute the population deviation of a list of populations.
    """

    max_pop: int = max(populations)
    min_pop: int = min(populations)

    return (max_pop - min_pop) / mean


def within_tolerance(diff_num: int, tolerance: int) -> bool:
    """
    Check if a population difference is within a tolerance .
    """

    return diff_num < tolerance and diff_num > -tolerance


class GeoID:
    """
    Parse 15-character GeoIDs into their component parts.
    """

    def __init__(self, id: str) -> None:
        self.state: str = id[0:2]
        self.county: str = id[0:5]  # id[2:5]
        self.tract: str = id[0:11]  # id[5:11]
        self.bg: str = id[0:12]  # id[11:12]
        self.block: str = id  # id[12:15]


#
