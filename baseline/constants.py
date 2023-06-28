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

baseline_maps: dict[str, str] = {
    "AL": "d16848f7-22a0-41a5-b19e-719923c54ee3",  # 06/27/23
    "AR": "c82e8e31-bd27-4f10-bf28-cf92a67a6c79",  # 06/27/23
    "AZ": "82cdf840-22b9-4af7-9e5a-0c6a17c4b88c",  # 06/27/23
    "CA": "239aeac7-3a09-4d6a-98d8-3de61f890b70",  # 06/27/23
    "CO": "867ed109-5f5b-4aa7-bc21-36f5d8b122c9",  # 06/27/23
    "CT": "1dbaa1de-68f0-4547-b6e9-db81617eb904",  # 06/27/23
    "FL": "25a30adb-d32e-4f5e-a45a-42b2e08183ef",  # 06/28/23
    "GA": "a44aa7ca-8fa0-43a2-9ba2-2b7f45a3c0f0",  # 06/28/23
    "IA": "7292b0dc-4911-4878-9960-68ae3a6abc10",  # 06/28/23
    "IL": "4dd9fe52-b38b-4f63-a041-36e3cd7afde0",  # 06/28/23
    "IN": "75a78afd-46b9-427f-9410-62204c3c5939",  # 06/27/23
    "KS": "9901f45d-6169-4577-ba9b-43c2fe2893d8",  # 06/28/23
    "KY": "a3a061bc-3178-4ae6-bdf0-a525ad6639b2",  # 06/28/23
    "LA": "e59f8d73-e552-4fd3-98d0-368722302720",  # 06/27/23
    "MA": "cfc4a446-c1d1-451e-affa-a79c52ea671e",  # 06/28/23
    "MD": "f6624aac-a170-4b52-a9b4-121322b12a9a",  # 06/28/23
    "MI": "0e074091-d3a7-4a79-bec7-a6c4641db018",  # 06/28/23
    "MN": "41893bfd-df1e-49b7-9322-6c134575dd35",  # 06/28/23
    "MO": "d1fdc45c-7d5e-45f5-af95-832094008465",  # 06/28/23
    "MS": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NC": "3fa75c2e-3790-483a-8664-2cc5e38250dc",  # 04/23/23
    "NE": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NJ": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NM": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NV": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "NY": "bea0efc4-52e7-4bbb-b942-67637ed4ab8a",  # 06/28/23
    "OH": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "OK": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "OR": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "PA": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "SC": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "TN": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "TX": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "UT": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "VA": "9981cdbe-ac6a-41f1-ab61-5ddebdd4f715",  # 04/06/23
    "WA": "8a1857af-5926-4371-acf5-321d233bdb04",  # 04/10/23
    "WI": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
}

### END ###
