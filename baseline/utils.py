#!/usr/bin/env python3

"""
UTILITIES - Not used at this time.
"""

import time
from functools import wraps
from typing import Any, Callable
from collections import namedtuple


# TIMER DECORATORS

# A decorator to report execution run time for freestanding functions.
def time_function(func) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tic: float = time.perf_counter()

        result: Any = func(*args, **kwargs)

        toc: float = time.perf_counter()
        print(f"{func.__name__} = {toc - tic: 0.1f} seconds")

        return result

    return wrapper


# A decorator to report execution run time for methods w/in classes
class Timer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def time_method(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_counter: float = time.process_time()  # perf_counter?

            result: Any = func(*args, **kwargs)

            end_counter: float = time.process_time()  # perf_counter?
            counter_time: float = end_counter - start_counter
            print(func.__name__, "=", "{:.10f}".format(counter_time), "seconds")

            return result

        return wrapper


# MISCELLANEOUS


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


class Pair(NamedTuple):
    one: int
    two: int

    def __repr__(self) -> str:
        return f"{self.one},{self.two}"


### END ###
