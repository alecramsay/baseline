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


# FILE NAMES & PATHS


def file_name(parts: list[str], delim: str = "_", ext: str = None) -> str:
    """
    Construct a file name with parts separated by the delimeter and ending with the extension.
    """
    name: str = delim.join(parts) + "." + ext if ext else delim.join(parts)

    return name


def path_to_file(parts: list[str], naked: bool = False) -> str:
    """
    Return the directory path to a file (but not the file).
    """

    rel_path: str = "/".join(parts)

    if not naked:
        rel_path = rel_path + "/"

    return rel_path


# TIMER DECORATORS

# A decorator to report execution run time for freestanding functions.
def time_function(func) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_counter: float = time.process_time()

        result: Any = func(*args, **kwargs)

        end_counter: float = time.process_time()
        counter_time: float = end_counter - start_counter
        print("...", func.__name__, "=", "{:.10f}".format(counter_time), "seconds")

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
