#!/usr/bin/env python3

"""
CONSTANTS
"""

from typing import Any
from pyutils import STATES, STATE_NAMES, STATE_FIPS


### PROJECT CONSTANTS ###

cycle: str = "2020"

study_states: list[str] = [
    "AL",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "FL",
    "GA",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "NE",
    "NV",
    "NJ",
    "NM",
    "NY",
    "NC",
    "OH",
    "OK",
    "OR",
    "PA",
    "SC",
    "TN",
    "TX",
    "UT",
    "VA",
    "WA",
    "WI",
]  # 37 states with > 2 congressional districts


### ENVIRONMENT CONSTANTS ###

rawdata_dir: str = "../../../local/pg/rawdata"
vtd_dir: str = "../../../local/vtd_data/2020_vtd"
data_dir: str = "data"
temp_dir: str = "temp"
intermediate_dir: str = "intermediate"
maps_dir: str = "maps"
dccvt_py: str = "../dccvt/examples/redistricting"
dccvt_go: str = "../dccvt/bin"


def unit_id(units: str) -> str:
    if units in ["block", "state", "vtd"]:
        return "GEOID20"
    if units in ["bg", "tract"]:
        return "GEOID"
    raise ValueError(f"Invalid units: {units}")


### STATE META DATA ###

# State code helpers copied from dra2020/data_tools/ by way of pyutils

# Districts by state -- built from dra-types/lib/stateinfo.ts (11/04/2022)

districts_by_state: dict[str, Any] = {
    "AL": {"congress": 7, "upper": 35, "lower": 105},
    "AK": {"congress": 1, "upper": 20, "lower": 40},
    "AZ": {"congress": 9, "upper": 30, "lower": None},
    "AR": {"congress": 4, "upper": 35, "lower": 100},
    "CA": {"congress": 52, "upper": 40, "lower": 80},
    "CO": {"congress": 8, "upper": 35, "lower": 65},
    "CT": {"congress": 5, "upper": 36, "lower": 151},
    "DE": {"congress": 1, "upper": 21, "lower": 41},
    "FL": {"congress": 28, "upper": 40, "lower": 120},
    "GA": {"congress": 14, "upper": 56, "lower": 180},
    "HI": {"congress": 2, "upper": 25, "lower": 51},
    "ID": {"congress": 2, "upper": 35, "lower": None},
    "IL": {"congress": 17, "upper": 59, "lower": 118},
    "IN": {"congress": 9, "upper": 50, "lower": 100},
    "IA": {"congress": 4, "upper": 50, "lower": 100},
    "KS": {"congress": 4, "upper": 40, "lower": 125},
    "KY": {"congress": 6, "upper": 38, "lower": 100},
    "LA": {"congress": 6, "upper": 39, "lower": 105},
    "ME": {"congress": 2, "upper": 35, "lower": 151},
    "MD": {"congress": 8, "upper": 47, "lower": 67},
    "MA": {"congress": 9, "upper": 40, "lower": 160},
    "MI": {"congress": 13, "upper": 38, "lower": 110},
    "MN": {"congress": 8, "upper": 67, "lower": 134},
    "MS": {"congress": 4, "upper": 52, "lower": 122},
    "MO": {"congress": 8, "upper": 34, "lower": 163},
    "MT": {"congress": 2, "upper": 50, "lower": 100},
    "NE": {"congress": 3, "upper": 49, "lower": None},
    "NV": {"congress": 4, "upper": 21, "lower": 42},
    "NH": {"congress": 2, "upper": 24, "lower": 164},
    "NJ": {"congress": 12, "upper": 40, "lower": None},
    "NM": {"congress": 3, "upper": 42, "lower": 70},
    "NY": {"congress": 26, "upper": 63, "lower": 150},
    "NC": {"congress": 14, "upper": 50, "lower": 120},
    "ND": {"congress": 1, "upper": 47, "lower": 49},
    "OH": {"congress": 15, "upper": 33, "lower": 99},
    "OK": {"congress": 5, "upper": 48, "lower": 101},
    "OR": {"congress": 6, "upper": 30, "lower": 60},
    "PA": {"congress": 17, "upper": 50, "lower": 203},
    "RI": {"congress": 2, "upper": 38, "lower": 75},
    "SC": {"congress": 7, "upper": 46, "lower": 124},
    "SD": {"congress": 1, "upper": 35, "lower": 37},
    "TN": {"congress": 9, "upper": 33, "lower": 99},
    "TX": {"congress": 38, "upper": 31, "lower": 150},
    "UT": {"congress": 4, "upper": 29, "lower": 75},
    "VT": {"congress": 1, "upper": 13, "lower": 104},
    "VA": {"congress": 11, "upper": 40, "lower": 100},
    "WA": {"congress": 10, "upper": 49, "lower": None},
    "WV": {"congress": 2, "upper": 17, "lower": 100},
    "WI": {"congress": 8, "upper": 33, "lower": 99},
    "WY": {"congress": 1, "upper": 31, "lower": 62},
}


# TODO - Log the resulting baseline maps here
baseline_maps: dict[str, str] = {
    "AL": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "AR": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "AZ": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "CA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "CO": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "CT": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "FL": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "GA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "IA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "IL": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "IN": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "KS": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "KY": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "LA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MD": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MI": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MN": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MO": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "MS": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NC": "48ea8e69-e6b8-4ddf-89f1-bcc65254ff00",  # 1000x = "a7ac927b-2dfc-4e79-b954-b9c43b7fe12f"
    "NE": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NJ": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NM": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NV": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NY": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "OH": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "OK": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "OR": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "PA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "SC": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "TN": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "TX": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "UT": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "VA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "WA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "WI": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
}

### END ###
