#!/usr/bin/env python3

"""
TEST EXCEL NAMING
"""


from baseline import *


class TestGraph:
    def test_is_consistent(self) -> None:
        data: dict[str, list[str]] = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        g: Graph = Graph(data)
        assert g._is_consistent()

        data: dict[str, list[str]] = {"a": ["b", "c"], "b": ["c"], "c": ["a", "b"]}
        g: Graph = Graph(data)
        try:
            g._is_consistent()
            assert False
        except:
            assert True


### END ###
