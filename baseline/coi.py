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

    if uom == -0.0:
        uom = 0.0

    return uom


def effective_splits(splits: list[float]) -> float:
    """Defined in Footnote 124 of the paper.

    Examples:
    - [0.33, 0.33, 0.34] => 2.00
    - [0.92, 0.05, 0.03] => 0.18
    """

    es: float = (1 / sum([x**2 for x in splits if x > 0])) - 1

    if es == -0.0:
        es = 0.0

    return es


def rate_uom(uom: float) -> int:
    """Rate uncertainty of membership [0–100] like DRA (Compare tab)

    The TypeScript implementation in DRA:

    function rateSplittingUncertainty(uncertainty: number): number
    {
    // See dra-analytics:
    // * The worst = 1.00 is [0.5, 0.5] splits (for every district) => rating of 0
    //               1.58 was districts split into thirds.
    // * The midpoint = 0.5                                         => rating of 50
    // * The best = 0.0 is a district preserved in it's entirety    => rating of 100

    const worst: number = 1.0;
    const scale: number = 100;

    let raw: number = uncertainty;
    let rating: number;

    raw = Math.min(Math.max(0, raw), worst);  // clip it
    raw = Math.abs(raw / worst);              // unitize it
    raw = 1 - raw;                            // invert it

    rating = Math.round(raw * scale);         // re-scale it

    return rating;
    }
    """

    worst: float = 1.0
    scale: int = 100

    raw: float = min(max(0, uom), worst)  # clip it
    raw = abs(raw / worst)  # unitize it
    raw = 1 - raw  # invert it

    rating: int = round(raw * scale)  # re-scale it

    return rating


### END ###
