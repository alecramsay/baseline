#!/usr/bin/env python3

"""
TEST COI METRICS
"""


from baseline.coi import uncertainty_of_membership, effective_splits
from pytest import approx


class TestCOI:
    def test_uncertainty_of_membership(self) -> None:
        assert uncertainty_of_membership([0.33, 0.33, 0.34]) == approx(1.59, abs=1e-2)
        assert uncertainty_of_membership([0.92, 0.05, 0.03]) == approx(0.48, abs=1e-2)

    def test_effective_splits(self) -> None:
        assert effective_splits([0.33, 0.33, 0.34]) == approx(2.00, abs=1e-2)
        assert effective_splits([0.92, 0.05, 0.03]) == approx(0.18, abs=1e-2)
