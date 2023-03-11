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

    def test_is_connected(self) -> None:
        geos: list[str] = ["a", "b", "c"]
        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b"],
        }
        assert is_connected(geos, adjacency)

        geos: list[str] = ["a", "b", "c", "d", "e", "f"]
        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b"],
            "d": ["e", "f"],
            "e": ["d", "f"],
            "f": ["d", "e"],
        }
        assert not is_connected(geos, adjacency)

        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b"],
        }
        g: Graph = Graph(adjacency)
        assert g.is_connected()


### END ###
