#!/usr/bin/env python3

"""
DEBUG
"""

from baseline import *


def main() -> None:
    xx: str = "NC"
    plan_type: str = "congress"

    verbose: bool = True

    baseline_state(xx, plan_type, "vtd", verbose)


if __name__ == "__main__":
    main()

### END ###
