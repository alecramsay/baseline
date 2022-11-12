#!/usr/bin/env python3
#
# HELPERS
#

import time
from functools import wraps
from typing import Any, Callable


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


#
