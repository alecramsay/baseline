#!/usr/bin/env python3

"""
TEST GRAPH FUNCTIONS
"""


from baseline.graph import Graph, is_connected


class TestGraph:
    def test_is_consistent(self) -> None:
        data: dict[str, list[str]] = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        g: Graph = Graph(data)
        assert g.is_consistent()

        data: dict[str, list[str]] = {"a": ["b", "c"], "b": ["c"], "c": ["a", "b"]}
        g: Graph = Graph(data)
        try:
            g.is_consistent()
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

    def test_remove(self) -> None:
        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b", "w"],
            "d": ["e", "f", "w"],
            "e": ["d", "f"],
            "f": ["d", "e"],
            "w": ["c", "d"],
        }
        g: Graph = Graph(adjacency)
        assert g.is_connected()
        before: int = len(g.nodes())

        g.remove("w")
        assert g.is_consistent()
        assert g.is_connected()
        after: int = len(g.nodes())
        assert before > after

    def test_add_adjacency(self) -> None:
        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b"],
            "d": ["e", "f"],
            "e": ["d", "f"],
            "f": ["d", "e"],
        }
        g: Graph = Graph(adjacency)
        assert not g.is_connected()

        g.add_adjacency("c", "d")
        assert g.is_consistent()
        assert g.is_connected()

    def test_adjacencies(self) -> None:
        data: dict[str, list[str]] = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        g: Graph = Graph(data)

        adjacencies: list[tuple[str, str]] = list(g.adjacencies())
        assert len(adjacencies) == 3

    def test_bridge(self) -> None:
        adjacency: dict[str, list[str]] = {
            "a": ["b", "c"],
            "b": ["a", "c"],
            "c": ["a", "b", "z"],
            "d": ["e", "f", "z"],
            "e": ["d", "f"],
            "f": ["d", "e"],
            "z": ["c", "d"],
        }
        g: Graph = Graph(adjacency)
        assert g.is_consistent()
        assert g.is_connected()
        assert "d" not in g.neighbors("c")
        assert "c" not in g.neighbors("d")

        g.bridge("z")
        assert g.is_consistent()
        assert g.is_connected()
        assert "d" in g.neighbors("c")
        assert "c" in g.neighbors("d")


### END ###
