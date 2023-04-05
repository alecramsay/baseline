#!/usr/bin/env python3

"""
COI SPLITTING

* Uncertainty of membership, and
* Effective splits

from:
"Turning Communities Of Interest Into A Rigorous Standard For Fair Districting" (Wang et al)
Stanford Journal of Civil Rights and Civil Liberties, Volume XVIII, Issue 1, pp.101-189, February 2022.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3828800
"""

import math


def uncertainty_of_membership(splits: list[float]) -> float:
    """Defined in Footnote 122 of the paper.

    Examples:
    - [0.33, 0.33, 0.34] => 1.59
    - [0.92, 0.05, 0.03] => 0.48
    """

    uom: float = -1 * sum([x * math.log2(x) for x in splits if x > 0])

    return uom


def effective_splits(splits: list[float]) -> float:
    """Defined in Footnote 124 of the paper.

    Examples:
    - [0.33, 0.33, 0.34] => 2.00
    - [0.92, 0.05, 0.03] => 0.18
    """

    es: float = (1 / sum([x**2 for x in splits if x > 0])) - 1

    return es
