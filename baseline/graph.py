#!/usr/bin/env python3

"""
ADJACENCY/CONTIGUITY GRAPHS
"""

import geopandas
from geopandas import GeoDataFrame

from libpysal.weights import Rook, WSP
from shapely.geometry import Polygon, MultiPolygon
from typing import Any, Optional

from .readwrite import *


OUT_OF_STATE: str = "OUT_OF_STATE"


class Graph:
    _data: dict
    _adjacencies: set[tuple[str, str]]

    def __init__(self, input: str | dict | GeoDataFrame, id_field: str = "") -> None:
        if isinstance(input, dict):
            self._data = input
            return

        if isinstance(input, str):
            self._abs_path: str = FileSpec(input).abs_path
            self._id_field: Optional[str] = id_field
            self._data: dict = self._from_shapefile()
            self.is_consistent()
            self._shp_by_geoid: dict
            self._meta: Optional[dict[str, Any]]
            self._shp_by_geoid, self._meta = read_shapes(self._abs_path, self._id_field)
            self._data: dict = self._add_out_of_state_neighbors()
            return

        if isinstance(input, GeoDataFrame):
            self._data: dict = self._from_dataframe(input)
            return

        raise TypeError("Input must be a string or a dict")

    def _from_shapefile(self) -> Any | dict[Any, Any]:
        """Extract a rook graph from a shapefile."""

        g: Rook | WSP = Rook.from_shapefile(self._abs_path, self._id_field)
        assert isinstance(g, Rook)

        return g.neighbors  # Get rid of all the extraneous PySAL stuff

    def _from_dataframe(self, df: GeoDataFrame) -> Any | dict[Any, Any]:
        """Extract a rook graph from a GeoDataFrame."""

        g: Rook | WSP = Rook.from_dataframe(df)
        assert isinstance(g, Rook)

        return g.neighbors  # Get rid of all the extraneous PySAL stuff

    def is_consistent(self) -> bool:
        """Make sure each node is in every neighbor's neighbor list"""

        for node, neighbors in self._data.items():
            for neighbor in neighbors:
                neighbor_neighbors: list[str | int] = self._data[neighbor]
                if node in neighbor_neighbors:
                    pass
                else:
                    return False

        return True

    def _add_out_of_state_neighbors(self) -> dict:
        """Add the virtual OUT_OF_STATE geoids to reflect interstate borders."""

        new_graph: dict = dict()
        new_graph[OUT_OF_STATE] = []
        epsilon: float = 1.0e-12

        for node, neighbors in self._data.items():
            new_graph[node] = []

            node_shp: Polygon | MultiPolygon = self._shp_by_geoid[node]
            perimeter: float = node_shp.length
            total_shared_border: float = 0.0

            for neighbor in neighbors:
                new_graph[node].append(neighbor)

                neighbor_shp: Polygon | MultiPolygon = self._shp_by_geoid[neighbor]
                shared_edge = node_shp.intersection(neighbor_shp)
                shared_border: float = shared_edge.length

                total_shared_border += shared_border

            if (perimeter - total_shared_border) > epsilon:
                new_graph[node].append(OUT_OF_STATE)
                new_graph[OUT_OF_STATE].append(node)

        return new_graph

    def data(self) -> dict:
        """Return the graph data."""

        return self._data

    def nodes(self) -> list[str | int]:
        """Return the nodes in the graph."""

        return list(self._data.keys())

    def neighbors(self, node: str | int, *, excluding: list = []) -> list[str | int]:
        """Return the neighbors of a node."""

        if node not in self._data:
            return []

        if len(excluding) == 0:
            return self._data[node]
        else:
            return [n for n in self._data[node] if n not in excluding]

    def is_border(self, node: str | int) -> bool:
        """Return True if the node is on the state boundary."""

        return OUT_OF_STATE in self._data[node]

    def is_connected(self) -> bool:
        """Return True if the graph is connected."""

        geos: list[str | int] = list(self._data.keys())
        adjacency: dict[str | int, list[str | int]] = self._data

        return is_connected(geos, adjacency)

    def add(self, node: str | int) -> None:
        """Add a node to the graph."""

        self._data[node] = []

    def connect(self, node1: str | int, node2: str | int) -> None:
        """Connect two nodes in the graph."""

        if node1 not in self._data or node2 not in self._data:
            raise ValueError("Both nodes must be in the graph to connect them.")

        self._data[node1].append(node2)
        self._data[node2].append(node1)

    def remove(self, node: str | int) -> None:
        """Remove a node from the graph maintaining its connectedness."""

        neighbors: list[str | int] = self._data[node]
        for neighbor in neighbors:
            self._data[neighbor].remove(node)
            for new_neighbor in neighbors:
                if (
                    new_neighbor != neighbor
                    and new_neighbor not in self._data[neighbor]
                ):
                    self._data[neighbor].append(new_neighbor)

        if node in self._data:
            del self._data[node]

    def add_adjacency(self, node1: str | int, node2: str | int) -> None:
        """Connect two nodes in the graph."""

        if node1 not in self._data or node2 not in self._data:
            raise ValueError("Both nodes must be in the graph to connect them.")

        self._data[node1].append(node2)
        self._data[node2].append(node1)

    def adjacencies(self) -> set[tuple[str, str]]:
        """Return unique pairs of adjacencent nodes in the graph."""

        n: int = 0
        self._adjacencies = set()

        for node, neighbors in self._data.items():
            for neighbor in neighbors:
                n += 1

                one: str = node if node < neighbor else neighbor
                two: str = neighbor if neighbor > node else node
                a: tuple[str, str] = (one, two)

                if a in self._adjacencies:
                    continue
                else:
                    self._adjacencies.add(a)

        if n != 2 * len(self._adjacencies):
            print(f"ERROR: Pairs of adjacencies are not consistent with the graph.")

        return self._adjacencies


### HELPERS ###


def border_shapes(
    district_ix: int,
    precincts: list[str],
    precinct_graph: Graph,
    districts_by_precinct: dict[str, set],  # Handles split precincts
) -> list[str]:
    """Return a list of *interior* border shapes for a district, i.e., not including those on the state boundary."""

    border: list[str] = list()

    for geoid in precincts:
        for neighbor in precinct_graph._data[geoid]:
            if neighbor == OUT_OF_STATE:
                border.append(geoid)
                break
            if len(districts_by_precinct[str(neighbor)]) > 1:
                continue  # Skip split precincts
            if district_ix != next(iter(districts_by_precinct[str(neighbor)])):
                border.append(geoid)
                break

    return border


def on_border_with(
    from_d: int,
    to_d: int,
    border: list[str],
    precinct_graph: Graph,
    districts_by_precinct: dict[str, set],  # Handles split precincts
) -> list:
    """Find precincts on the border of one district with another."""

    candidates: list[str] = list()

    for geoid in border:
        for neighbor in precinct_graph._data[geoid]:
            if neighbor == OUT_OF_STATE:
                continue
            if len(districts_by_precinct[str(neighbor)]) > 1:
                continue  # Skip split precincts
            if to_d == next(iter(districts_by_precinct[str(neighbor)])):
                candidates.append(geoid)
                break

    return candidates


def is_connected(geos: list[Any], adjacency: dict[Any, list[Any]]) -> bool:
    """Make sure a graph is fully connected *internally*, i.e., w/o regard to the virtual state boundary "shapes".

    Kenshi's iterative implementation of the recursive algorithm

    geos - the list of geographies
    adjacency - the connectedness of the geos
    """
    visited: set[Any] = set()

    all_geos: set[Any] = set(geos)
    all_geos.discard(OUT_OF_STATE)

    start: str = next(iter(all_geos))
    assert start != OUT_OF_STATE

    to_process: list[Any] = [start]
    while to_process:
        node: Any = to_process.pop()
        visited.add(node)
        neighbors: list[Any] = list(adjacency[node])
        if OUT_OF_STATE in neighbors:
            neighbors.remove(OUT_OF_STATE)
        neighbors_to_visit: list[Any] = [
            n for n in neighbors if n in all_geos and n not in visited
        ]
        to_process.extend(neighbors_to_visit)

    return len(visited) == len(all_geos)


"""
The original graph modification code from the dra2020/data_tools Python script:

def modify_graph(graph, mods_csv) -> dict[str, list]:
    # Mod column indexes
    OP: int = 0
    FROM: int = 1
    TO: int = 2

    mods: list = read_mods(mods_csv)

    for mod in mods:
        if mod[OP] == "+":
            graph[mod[FROM]].append(mod[TO])
            graph[mod[TO]].append(mod[FROM])
        elif mod[OP] == "-":
            print("Removing connections is not supported yet.")
        else:
            print("Unrecognized modify operator.")

    return graph


def read_mods(mods_csv) -> list:
    mods: list = list()

    try:
        # Get the full path to the .csv
        mods_path: str = os.path.expanduser(mods_csv)

        with open(mods_path, mode="r", encoding="utf-8-sig") as f_input:
            reader: Iterable[list[str]] = csv.reader(
                f_input, skipinitialspace=True, delimiter=",", quoting=csv.QUOTE_NONE
            )

            for row in reader:
                mods.append(row)

    except Exception:
        print("Exception reading mods.csv")
        sys.exit()

    return mods
    
"""


### END ###
