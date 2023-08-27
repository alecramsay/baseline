#!/usr/bin/env python3

"""
READ/WRITE routines
"""

import json
from collections import defaultdict
from shapely.geometry import (
    shape,
    Polygon,
    MultiPolygon,
)
from typing import Any, Optional

from pyutils import (
    FileSpec,
    file_name,
    path_to_file,
    read_csv,
    write_csv,
    read_json,
    read_shapes,
    write_pickle,
    read_pickle,
)


### LOAD & PROCESS CENSUS DATA ###


def read_census_json(rel_path) -> defaultdict[str, int]:
    """Read the DRA census block data JSON for a state, and extract the population."""

    abs_path: str = FileSpec(rel_path).abs_path
    with open(abs_path, "r", encoding="utf-8-sig") as f:
        data: Any = json.load(f)

    dataset_key: str = "D20F"
    field: str = "Tot"
    pop_by_geoid: defaultdict[str, int] = defaultdict(int)
    for feature in data["features"]:
        geoid: str = feature["properties"]["GEOID"]
        pop: int = feature["properties"]["datasets"][dataset_key][field]

        pop_by_geoid[geoid] = pop

    return pop_by_geoid


### LOAD A STATE SHAPEFILE ###


def load_state_shape(shp_file: str, id: str) -> Polygon | MultiPolygon:
    shapes: tuple[dict, Optional[dict[str, Any]]] = read_shapes(shp_file, id)
    state_shp: Polygon | MultiPolygon = list(shapes[0].items())[0][1]

    return state_shp


### END ###
