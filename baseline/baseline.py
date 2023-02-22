#!/usr/bin/env python3

"""
BASELINE DISTRICTS
"""

import os

from .constants import *
from .utils import *
from .readwrite import *


@time_function
def baseline_with_bgs(xx: str, plan_type: str, verbose: bool = False) -> None:
    """Find baseline districts for a state"""

    map_label: str = label_map(xx, plan_type)
    print(f"Generating baseline map for {map_label}:")

    input_csv: str
    points_csv: str
    sites_csv: str
    initial_csv: str
    balzer_csv: str
    consolidated_csv: str
    centroids_csv: str
    output_csv: str

    # 1 - Run repeated runs using blockgroups & random seeds.

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "bg", "data"])

    points_csv = full_path([intermediate_dir, xx], [map_label, "bg", "points"])
    make_points(input_csv, points_csv)

    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # TODO: make this a parameter
    fips_map: dict[str, str] = make_state_codes()
    fips: str = fips_map[xx]

    start: int = K * N * int(fips)
    iterations: int = 100

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        print(f"... Iteration: {iter_label}, seed: {seed} ...")

        sites_csv = full_path(
            [intermediate_dir, xx], [map_label, "bg", iter_label, "sites"]
        )
        initial_csv = full_path(
            [intermediate_dir, xx], [map_label, "bg", iter_label, "initial"]
        )
        balzer_csv = full_path(
            [intermediate_dir, xx], [map_label, "bg", iter_label, "balzer"]
        )
        centroids_csv = full_path(
            [intermediate_dir, xx], [map_label, "bg", iter_label, "centroids"]
        )

        make_sites(points_csv, sites_csv, seed, K * N)
        make_initial(sites_csv, points_csv, initial_csv)
        run_dccvt(sites_csv, points_csv, initial_csv, balzer_csv)
        get_sites(points_csv, balzer_csv, centroids_csv)

    # 2 - Find characteristic sites (district centroids) resulting from the BG runs.

    print(f"... Finding characteristic sites ...")

    centroids_pattern: str = full_path(
        [intermediate_dir, xx], [map_label, "bg", "*", "centroids"]
    )
    points_csv = full_path(
        [intermediate_dir, xx], [map_label, "characteristic", "points"]
    )
    sites_csv = full_path(
        [intermediate_dir, xx], [map_label, "characteristic", "sites"]
    )
    initial_csv = full_path(
        [intermediate_dir, xx], [map_label, "characteristic", "initial"]
    )
    balzer_csv = full_path(
        [intermediate_dir, xx], [map_label, "characteristic", "balzer"]
    )
    centroids_csv = full_path(
        [intermediate_dir, xx], [map_label, "characteristic", "centroids"]
    )

    combine_centroids(centroids_pattern, points_csv)
    make_sites(points_csv, sites_csv, start + iterations + 1, K * N)
    make_initial(sites_csv, points_csv, initial_csv)
    run_dccvt(sites_csv, points_csv, initial_csv, balzer_csv)
    get_sites(points_csv, balzer_csv, centroids_csv)

    # 3 - Do a final clean up run:
    # * Use blocks instead of blockgroups.
    # * Use the characteristic sites instead of random ones
    # * Snap each block one and only one district.
    # * Generate a block-assignment file.

    print(f"... Final clean up run ...")

    input_csv: str = full_path([data_dir, xx], [xx, cycle, "block", "data"])
    points_csv = full_path([intermediate_dir, xx], [map_label, "block", "points"])
    initial_csv = full_path([intermediate_dir, xx], [map_label, "block", "initial"])
    balzer_csv = full_path([intermediate_dir, xx], [map_label, "block", "balzer"])
    consolidated_csv = full_path(
        [intermediate_dir, xx], [map_label, "block", "consolidated"]
    )
    complete_csv: str = full_path(
        [intermediate_dir, xx], [map_label, "block", "complete"]
    )
    output_csv: str = full_path([maps_dir], [map_label, "baf"])

    make_points(input_csv, points_csv)
    # sites_csv = centroids_csv from previous step
    make_initial(centroids_csv, points_csv, initial_csv)
    run_dccvt(centroids_csv, points_csv, initial_csv, balzer_csv)
    consolidate_balzer(balzer_csv, consolidated_csv)
    handle_unassigned(consolidated_csv, points_csv, balzer_csv, complete_csv)
    make_baf(input_csv, complete_csv, output_csv)

    pass


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


def make_baf(input_csv: str, complete_csv: str, baf_csv: str) -> None:
    """Make a block-assignment file from a file of unique assignments of blocks to districts (sites)

    python3 redistricting.py postprocess --redistricting_input redistricting.csv --input consolidated.csv --output output.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py postprocess --redistricting_input {input_csv} --input {complete_csv} --output {baf_csv}"
    os.system(command)


def get_sites(points_csv: str, baf_csv: str, centroids_csv: str) -> None:
    """Get *ending* sites (district centroids) from assignments

    python3 redistricting.py centroids --points point.csv  --assignment balzer.csv --centroids centroids.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py centroids --points {points_csv}  --assignment {baf_csv} --centroids {centroids_csv}"
    os.system(command)


def combine_centroids(inputs: str, output: str) -> None:
    """Concatenate all BG centroids.csv into one file

    cat NC20C_bg_*_centroids.csv > NC20C_block_sites.csv
    """

    command: str = f"cat {inputs} > {output}"
    os.system(command)


def handle_unassigned(
    consolidated_csv: str, points_csv: str, balzer_csv: str, complete_csv: str
) -> None:
    """Handle unassigned zero-population blocks

    python3 redistricting.py complete --assignment consolidated.csv --points points.csv --balzer balzer.csv --output complete.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py complete --assignment {consolidated_csv} --points {points_csv} --balzer {balzer_csv} --output {complete_csv}"
    os.system(command)


### HELPER FUNCTIONS ###


def full_path(dirs: list[str], file_parts: list[str]) -> str:
    """Return a fully qualifed file name from a list of directories and a list of file parts"""

    rel_path: str = path_to_file(dirs) + file_name(file_parts, "_", "csv")
    return FileSpec(rel_path).abs_path


def label_map(xx: str, plan_type: str) -> str:
    return f"{xx}{cycle[2:]}{plan_type.upper()[0]}"


def label_iteration(I: int, K: int, N: int) -> str:
    return f"I{I:02d}K{K:02d}N{N:02d}"


### END ###
