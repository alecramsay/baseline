#!/usr/bin/env python3

"""
ADJACENCY/CONTIGUITY GRAPHS
"""

import os
import sys
import csv
from csv import reader as _reader
from libpysal.weights import Rook

from .readwrite import *


def graph_shapes(rel_path: str, id_field: str) -> Rook:
    """Extract a rook graph from a shapefile."""

    abs_path: str = FileSpec(rel_path).abs_path

    g: Rook = Rook.from_shapefile(abs_path, id_field)
    g = g.neighbors  # Get rid of all the extraneous PySAL stuff

    return g


def check_graph(graph) -> bool:
    """Make sure each node is in every neighbor's neighbor list"""

    consistent: bool = True

    for from_geo, neighbor_geos in graph.items():
        for to_geo in neighbor_geos:
            neighbors_neighbors: list[str] = graph[to_geo]
            if from_geo in neighbors_neighbors:
                pass
            else:
                consistent = False

    return consistent


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


def id_border_units(
    id: int,
    units: list[str],
    unit_graph: dict[str, list[str]],
    district_by_geoid: dict[str, int],
) -> list[str]:
    """Return a list of *interior* border units for a district, i.e., not including units on the state boundary."""

    border: list[str] = list()

    for unit in units:
        for neighbor in unit_graph[unit]:
            if district_by_geoid[neighbor] != id:
                border.append(unit)
                break

    return border


### END ###
