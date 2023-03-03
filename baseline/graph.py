#!/usr/bin/env python3

"""
ADJACENCY/CONTIGUITY GRAPHS
"""

import os
import sys
import csv
from csv import reader as _reader
from libpysal.weights import Rook
import fiona
import shapely.geometry
from shapely.geometry import shape, Polygon, MultiPolygon

from .readwrite import *


OUT_OF_STATE: str = "OUT_OF_STATE"


class Graph:
    def __init__(self, input: str | dict, id_field: str = None) -> None:
        if isinstance(input, dict):
            self._data: dict = input
            return

        if isinstance(input, str):
            self._abs_path: str = FileSpec(input).abs_path
            self._id_field: str = id_field
            self._data: dict = self._from_shapefile()
            self._is_consistent()
            self._shp_by_geoid: dict
            self._meta: dict[str, Any]
            self._shp_by_geoid, self._meta = load_shapes(self._abs_path, self._id_field)
            self._data: dict = self._add_out_of_state_neighbors()

            return

        raise TypeError("Input must be a string or a dict")

    def _from_shapefile(self) -> Rook:
        """Extract a rook graph from a shapefile."""

        g: Rook = Rook.from_shapefile(self._abs_path, self._id_field)
        return g.neighbors  # Get rid of all the extraneous PySAL stuff

    def _is_consistent(self) -> bool:
        """Make sure each node is in every neighbor's neighbor list"""

        consistent: bool = True

        for node, neighbors in self._data.items():
            for neighbor in neighbors:
                neighbor_neighbors: list[str] = self.neighbors(neighbor)
                if node in neighbor_neighbors:
                    pass
                else:
                    raise ValueError("Graph is not internally consistent!")

        return consistent

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

    def neighbors(self, node: str) -> list[str]:
        """Return the neighbors of a node."""

        if node in self._data:
            return self._data[node]
        else:
            return []


### HELPERS ###


def border_shapes(
    district_ix: int,
    units: list[str],
    unit_graph: Graph,
    district_by_geoid: dict[str, int],
) -> list[str]:
    """Return a list of *interior* border shapes for a district, i.e., not including those on the state boundary."""

    border: list[str] = list()

    for geoid in units:
        for neighbor in unit_graph.neighbors(geoid):
            if neighbor == OUT_OF_STATE:
                border.append(geoid)
                break
            if district_by_geoid[neighbor] != district_ix:
                border.append(geoid)
                break

    return border


# TODO - Integrate these into the class


def modify_graph(graph, mods_csv) -> dict[str, list]:
    """Modify & return a graph."""

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
    """
    +, 440099902000, 440099901000
    """

    mods: list = list()

    try:
        # Get the full path to the .csv
        mods_csv: str = os.path.expanduser(mods_csv)

        with open(mods_csv, mode="r", encoding="utf-8-sig") as f_input:
            reader: _reader = csv.reader(
                f_input, skipinitialspace=True, delimiter=",", quoting=csv.QUOTE_NONE
            )

            for row in reader:
                mods.append(row)

    except Exception as e:
        print("Exception reading mods.csv")
        sys.exit(e)

    return mods


### END ###
