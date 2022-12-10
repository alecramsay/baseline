#!/usr/bin/env python3
#
# I/O HELPERS
#

import os
import json
from csv import DictReader, DictWriter
import pickle
from collections import defaultdict
from shapely.geometry import shape, Polygon, MultiPolygon
import fiona
from typing import Any, Optional


### LOAD & PROCESS CENSUS DATA ###


def read_census_json(rel_path) -> defaultdict[str, int]:
    """
    Read the DRA census block data JSON for a state, and extract the population.
    """

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


def load_json(rel_path) -> dict[str, Any]:
    abs_path: str = FileSpec(rel_path).abs_path

    with open(abs_path, "r") as f:
        return json.load(f)


### LOAD A SHAPEFILE ###


def load_shapes(shp_file: str, id: str) -> tuple[dict, dict[str, Any]]:
    shp_file: str = os.path.expanduser(shp_file)
    shapes_by_id: dict = dict()

    with fiona.Env():
        with fiona.open(shp_file) as source:
            meta: dict[str, Any] = source.meta
            for item in source:
                obj_id: str = item["properties"][id]
                shp: Polygon | MultiPolygon = shape(item["geometry"])

                shapes_by_id[obj_id] = shp

    return shapes_by_id, meta


def load_state_shape(shp_file: str, id: str) -> Polygon | MultiPolygon:
    shapes: tuple[dict, dict[str, Any]] = load_shapes(shp_file, id)
    state_shp: Polygon | MultiPolygon = list(shapes[0].items())[0][1]

    return state_shp


### READ & WRITE A CSV ###


def write_csv(rel_path, rows, cols, precision="{:.6f}") -> None:
    try:
        abs_path: str = FileSpec(rel_path).abs_path

        with open(abs_path, "w") as f:
            writer: DictWriter = DictWriter(f, fieldnames=cols)
            writer.writeheader()

            for row in rows:
                mod: dict = {}
                for (k, v) in row.items():
                    if isinstance(v, float):
                        mod[k] = precision.format(v)
                    else:
                        mod[k] = v
                writer.writerow(mod)

    except:
        raise Exception("Exception writing CSV.")


def read_typed_csv(rel_path, field_types) -> list:
    """
    Read a CSV with DictReader
    Patterned after: https://stackoverflow.com/questions/8748398/python-csv-dictreader-type
    """

    abs_path: str = FileSpec(rel_path).abs_path

    try:
        rows: list = []
        with open(abs_path, "r", encoding="utf-8-sig") as file:
            reader: DictReader[str] = DictReader(
                file, fieldnames=None, restkey=None, restval=None, dialect="excel"
            )

            for row_in in reader:
                if len(field_types) >= len(reader.fieldnames):
                    # Extract the values in the same order as the csv header
                    ivalues = map(row_in.get, reader.fieldnames)

                    # Apply type conversions
                    iconverted: list = [
                        cast(x, y) for (x, y) in zip(field_types, ivalues)
                    ]

                    # Pass the field names and the converted values to the dict constructor
                    row_out: dict = dict(zip(reader.fieldnames, iconverted))

                rows.append(row_out)

        return rows

    except:
        raise Exception("Exception reading CSV with explicit types.")


def cast(t, v_str) -> str | int | float:
    return t(v_str)


### PICKLING & UNPICKLING ###


def write_pickle(rel_path, obj) -> bool:
    abs_path: str = FileSpec(rel_path).abs_path

    try:
        with open(abs_path, "wb") as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True
    except Exception as e:
        print("Exception pickling: ", e)
        return False


def read_pickle(rel_path) -> Optional[bytes]:
    abs_path: str = FileSpec(rel_path).abs_path

    try:
        with open(abs_path, "rb") as handle:
            return pickle.load(handle)
    except Exception as e:
        print("Exception unpickling: ", e)
        return None


### FILE NAMES & PATHS ###


class FileSpec:
    def __init__(self, path: str, name=None) -> None:
        file_name: str
        file_extension: str
        file_name, file_extension = os.path.splitext(path)

        self.rel_path: str = path
        self.abs_path: str = os.path.abspath(path)
        self.name: str = name.lower() if (name) else os.path.basename(file_name).lower()
        self.extension: str = file_extension


def file_name(parts: list[str], delim: str = "_", ext: str = None) -> str:
    """
    Construct a file name with parts separated by the delimeter and ending with the extension.
    """
    name: str = delim.join(parts) + "." + ext if ext else delim.join(parts)

    return name


def path_to_file(parts: list[str], naked: bool = False) -> str:
    """
    Return the directory path to a file (but not the file).
    """

    rel_path: str = "/".join(parts)

    if not naked:
        rel_path = rel_path + "/"

    return rel_path


### NOTUSED ###

"""
LEGACY

def load_census(c_csv, id: str, pop: str) -> defaultdict[str, int]:
    try:
        # READ STANDARD CENSUS DATA FROM A .CSV FILE
        census_by_geoID: defaultdict[str, int] = read_census_csv(c_csv, id, pop)
    except Exception as e:
        sys.exit(e)

    return census_by_geoID
	
def read_census_csv(census_csv: str, id: str, pop: str) -> defaultdict[str, int]:
    # Get the full path to the .csv
    census_csv: str = os.path.expanduser(census_csv)

    # Initialize an index of Census data by geo
    census_by_geoID: defaultdict[str, int] = defaultdict(int)

    with open(census_csv) as f_input:
        csv_file: DictReader[str] = DictReader(f_input)

        # Process each row in the .csv file
        for row in csv_file:
            # Subset the row to the desired columns
            geoID: str = row[id]
            total: int = int(row[pop])

            # and write the values out into a dictionary
            census_by_geoID[geoID] = total

    return census_by_geoID
"""
