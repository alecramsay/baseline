#!/usr/bin/env python3

"""
BASELINE DISTRICTS
"""

import os

from .constants import *
from .readwrite import *


def baseline_state(xx: str, plan_type: str, verbose: bool = False) -> None:
    """Find baseline districts for a state.

    Find characteristic sites, using blockgroups: <<< TODO: Compare using sample blocks
    - Convert BG data to X_points.csv
    - For each of 100 iterations:
        - Create X_sites.csv using X_points.csv & a random seed
        - Create X_initial.csv using X_sites.csv
        - Run dccvt to create X_assignments.csv
        - Create district X_sites.csv
    - Use all the X_centroids.csv to find characteristic sites
    - Fin
    """

    # Do one end-to-end run

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "bg", "data"])
    points_csv: str = full_path([intermediate_dir, xx], [xx, cycle, "points"])
    sites_csv: str = full_path([intermediate_dir, xx], [xx, cycle, "sites"])
    initial_csv: str = full_path([intermediate_dir, xx], [xx, cycle, "initial"])
    balzer_csv: str = full_path([intermediate_dir, xx], [xx, cycle, "balzer"])
    consolidated_csv: str = full_path(
        [intermediate_dir, xx], [xx, cycle, "consolidated"]
    )
    centroids_csv: str = full_path([intermediate_dir, xx], [xx, cycle, "centroids"])
    output_csv: str = full_path([maps_dir], [xx, cycle, plan_type])

    make_points(input_csv, points_csv)
    make_sites(points_csv, sites_csv, 31415, 14)
    make_initial(sites_csv, points_csv, initial_csv)
    run_dccvt(sites_csv, points_csv, initial_csv, balzer_csv)
    consolidate_balzer(balzer_csv, consolidated_csv)
    make_baf(input_csv, consolidated_csv, output_csv)
    get_sites(points_csv, balzer_csv, centroids_csv)

    pass  # TODO


### DCCVT WRAPPERS ###


def make_points(input_csv: str, points_csv) -> None:
    """Create points.csv from preferred redistricting input.csv format

    python3 redistricting.py points --input redistricting.csv --output points.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py points --input {input_csv} --output {points_csv}"
    os.system(command)


def make_sites(points_csv: str, sites_csv: str, seed: int, n: int) -> None:
    """Create starting sites from points.csv

    python3 redistricting.py sites --points points.csv --output sites.csv --seed 31415 --N 14
    """

    command: str = f"python3 {dccvt_py}/redistricting.py sites --points {points_csv} --output {sites_csv} --seed {seed} --N {n}"
    os.system(command)


def make_initial(sites_csv: str, points_csv: str, initial_csv: str) -> None:
    """Create starting sites from points.csv

    python3 redistricting.py initial --sites sites.csv --points points.csv --output initial.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py initial --sites {sites_csv} --points {points_csv} --output {initial_csv}"
    os.system(command)


def run_dccvt(
    sites_csv: str, points_csv: str, initial_csv: str, balzer_csv: str
) -> None:
    """Run dccvt

    ../../bin/dccvt --sites sites.csv --points points.csv --initial initial.csv --output balzer.csv
    """

    command: str = f"{dccvt_go}/dccvt --sites {sites_csv} --points {points_csv} --initial {initial_csv} --output {balzer_csv}"
    os.system(command)


def consolidate_balzer(balzer_csv: str, consolidated_csv: str) -> None:
    """Consolidate potentially fractional/split assignments in balzer.csv to unique assignments in consolidated.csv

    python3 redistricting.py consolidate --input balzer.csv --output consolidated.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py consolidate --input {balzer_csv} --output {consolidated_csv}"
    os.system(command)


def make_baf(input_csv: str, consolidated_csv: str, baf_csv: str) -> None:
    """Make a block-assignment file from a file of unique assignments of blocks to districts (sites)

    python3 redistricting.py postprocess --redistricting_input redistricting.csv --input consolidated.csv --output output.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py postprocess --redistricting_input {input_csv} --input {consolidated_csv} --output {baf_csv}"
    os.system(command)


def get_sites(points_csv: str, baf_csv: str, centroids_csv: str) -> None:
    """Get *ending* sites (district centroids) from assignments

    python3 redistricting.py centroids --points point.csv  --assignment balzer.csv --centroids centroids.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py centroids --points {points_csv}  --assignment {baf_csv} --centroids {centroids_csv}"
    os.system(command)


### HELPER FUNCTIONS ###


def full_path(dirs: list[str], file_parts: list[str]) -> str:
    """Return a fully qualifed file name from a list of directories and a list of file parts"""

    rel_path: str = path_to_file(dirs) + file_name(file_parts, "_", "csv")
    return FileSpec(rel_path).abs_path


### END ###
