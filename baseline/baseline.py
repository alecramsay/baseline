#!/usr/bin/env python3

"""
BASELINE DISTRICTS
"""

import os

from .constants import *
from .utils import *
from .readwrite import *


def do_baseline_run(
    tmpdir: str,
    N: int,
    seed: int,
    prefix: str,
    data: str,
    adjacencies: str,
    output: str,
    label: str,
    verbose: bool = False,
) -> None:
    """Make a set of baseline districts from random starting sites

    Do this many times, and then choose the baseline as the map with the lowest energy.
    """

    command: str = f"create.sh --tmpdir={tmpdir} --N={N} --seed={seed} --prefix={prefix} --data={data} --adjacencies={adjacencies} --output={output} --label={label}"
    os.system(command)


### RESTORED ###


@time_function
def baseline_state_iterative(
    xx: str, plan_type: str, iter_unit: str, finish_unit: str, verbose: bool = False
) -> None:
    """Find baseline districts for a state using iter_unit x 100 and finish_unit once."""

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

    # 1 - Run repeated runs using VTDs & random seeds.

    input_csv: str = full_path([data_dir, xx], [xx, cycle, iter_unit, "data"])

    points_csv = full_path([intermediate_dir, xx], [map_label, iter_unit, "points"])
    create_points_file(input_csv, points_csv)

    N: int = districts_by_state[xx][plan_type]
    K: int = 1  # TODO: make this a parameter
    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    start: int = K * N * int(fips)
    iterations: int = 100

    for i, seed in enumerate(range(start, start + iterations)):
        iter_label: str = label_iteration(i, K, N)
        print(f"... Iteration: {iter_label}, seed: {seed} ...")

        sites_csv = full_path(
            [intermediate_dir, xx], [map_label, iter_unit, iter_label, "sites"]
        )
        initial_csv = full_path(
            [intermediate_dir, xx], [map_label, iter_unit, iter_label, "initial"]
        )
        balzer_csv = full_path(
            [intermediate_dir, xx], [map_label, iter_unit, iter_label, "balzer"]
        )
        centroids_csv = full_path(
            [intermediate_dir, xx], [map_label, iter_unit, iter_label, "centroids"]
        )

        create_random_sites_file(points_csv, sites_csv, seed, K * N)
        create_initial_assignment_file(sites_csv, points_csv, initial_csv)
        run_balzer(sites_csv, points_csv, initial_csv, balzer_csv)
        get_centroids_file(points_csv, balzer_csv, centroids_csv)

    # 2 - Find characteristic sites (district centroids) resulting from the random-seed runs.

    print(f"... Finding characteristic sites ...")

    centroids_pattern: str = full_path(
        [intermediate_dir, xx], [map_label, iter_unit, "*", "centroids"]
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

    combine_centroids_files(centroids_pattern, points_csv)
    create_random_sites_file(points_csv, sites_csv, start + iterations + 1, K * N)
    create_initial_assignment_file(sites_csv, points_csv, initial_csv)
    run_balzer(sites_csv, points_csv, initial_csv, balzer_csv)
    get_centroids_file(points_csv, balzer_csv, centroids_csv)

    # 3 - Do a final clean up run:
    # * Use VTDs again, but
    # * Use the characteristic sites instead of random ones
    # * Snap each VTD to one and only one district.
    # * Generate a VTD-assignment file.

    print(f"... Final clean up run ...")

    input_csv: str = full_path([data_dir, xx], [xx, cycle, finish_unit, "data"])
    points_csv = full_path([intermediate_dir, xx], [map_label, finish_unit, "points"])
    initial_csv = full_path([intermediate_dir, xx], [map_label, finish_unit, "initial"])
    balzer_csv = full_path([intermediate_dir, xx], [map_label, finish_unit, "balzer"])
    consolidated_csv = full_path(
        [intermediate_dir, xx], [map_label, finish_unit, "consolidated"]
    )
    complete_csv: str = full_path(
        [intermediate_dir, xx], [map_label, finish_unit, "complete"]
    )
    output_csv: str = full_path([maps_dir], [map_label, finish_unit, "baf"])

    create_points_file(input_csv, points_csv)
    # sites_csv = centroids_csv from previous step
    create_initial_assignment_file(centroids_csv, points_csv, initial_csv)
    run_balzer(centroids_csv, points_csv, initial_csv, balzer_csv)
    create_consolidated_file(balzer_csv, consolidated_csv)
    create_complete_file(consolidated_csv, points_csv, balzer_csv, complete_csv)
    create_output_file(input_csv, complete_csv, output_csv)

    pass


### DCCVT WRAPPERS ###


def create_points_file(input_csv: str, points_csv) -> None:
    """Create points.csv from preferred redistricting input.csv format

    python3 geoid.py points --input redistricting.csv --output points.csv
    """

    command: str = (
        f"python3 {dccvt_py}/geoid.py points --input {input_csv} --output {points_csv}"
    )
    os.system(command)


def create_random_sites_file(
    points_csv: str, sites_csv: str, seed: int, n: int
) -> None:
    """Create random sites from points.csv

    python3 redistricting.py sites --points points.csv --output sites.csv --seed 31415 --N 14
    """

    command: str = f"python3 {dccvt_py}/redistricting.py sites --points {points_csv} --output {sites_csv} --seed {seed} --N {n}"
    os.system(command)


def create_initial_assignment_file(
    sites_csv: str, points_csv: str, initial_csv: str
) -> None:
    """Create starting sites from points.csv

    python3 redistricting.py initial --sites sites.csv --points points.csv --output initial.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py initial --sites {sites_csv} --points {points_csv} --output {initial_csv}"
    os.system(command)


def run_balzer(
    points_csv: str,
    initial_csv: str,
    adjacencies_csv: str,
    threshold: int,
    balzer_csv: str,
) -> None:
    """Run Balzer

    ../../bin/dccvt --sites sites.csv --points points.csv --initial initial.csv --output balzer.csv
    """

    command: str = f"{dccvt_go}/dccvt --points {points_csv} --initial {initial_csv} --adjacencies {adjacencies_csv} --output {balzer_csv}"
    os.system(command)


def create_unbalanced_contiguous_assignment_file(
    assignment_csv: str, adjacencies_csv: str, unbalanced_csv: str
) -> None:
    """Create an unbalanced contiguous assignment file

    python3 redistricting.py contiguous \
        --assignment "$balzer_balanced_noncontiguous_assignmentfile" \
        --adjacent "$adjacenciesfile" \
        --output "$unbalanced_contiguous_assignmentfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py contiguous --assignment {assignment_csv} --adjacent {adjacencies_csv} --output {unbalanced_csv}"
    os.system(command)


def create_balanced_contiguous_assignment_file(
    assignment_csv: str, adjacencies_csv: str, max_iterations: int, balanced_csv: str
) -> None:
    """Create a balanced contiguous assignment file

    python3 redistricting.py rebalance \
        --assignment "$balzer_unbalanced_contiguous_assignmentfile" \
        --adjacent "$adjacenciesfile" \
        --max_iterations 1000 \
        --output "$balanced_contiguous_assignmentfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py rebalance --assignment {assignment_csv} --adjacent {adjacencies_csv} --max_iterations {max_iterations} --output {balanced_csv}"
    os.system(command)


def create_consolidated_file(
    assignment_csv: str, adjacencies_csv: str, label: str, consolidated_csv: str
) -> None:
    """Consolidate potentially fractional/split assignments in balzer.csv to unique assignments in consolidated.csv

    python3 redistricting.py consolidate \
    --assignment "$balzer_balanced_contiguous_assignmentfile" \
    --adjacent "$adjacenciesfile" \
    --label "$label" \
    --output "$consolidatedfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py consolidate --assignment {assignment_csv} --adjacent {adjacencies_csv} --label {label} --output {consolidated_csv}"
    os.system(command)


def create_complete_file(
    consolidated_csv: str,
    adjacencies_csv: str,
    points_csv: str,
    complete_csv: str,
) -> None:
    """Create complete file

    python3 redistricting.py complete \
        --assignment "$consolidatedfile" \
        --adjacent "$adjacenciesfile" \
        --points "$pointsfile" \
        --output "$completefile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py complete --assignment {consolidated_csv} --adjacent {adjacencies_csv} --points {points_csv} --output {complete_csv}"
    os.system(command)


def compute_energy(assignment_csv: str, points_csv: str, label: str) -> None:
    """Computing energy of a completed map

    python3 redistricting.py energy \
        --assignment "$completefile" \
        --points "$pointsfile" \
        --label "$label"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py energy --assignment {assignment_csv} --points {points_csv} --label {label}"
    os.system(command)


def create_output_file(input_csv: str, complete_csv: str, baf_csv: str) -> None:
    """Make an assignment file from a file of unique assignments of VTDs (or blocks) to districts (sites)

    python3 geoid.py postprocess --input complete.csv --redistricting_input redistricting.csv --output output.csv

    $GEOID postprocess \
    --input "$completefile" \
    --redistricting_input "$infile" \
    --output "$outfile"
    """

    command: str = f"python3 {dccvt_py}/geoid.py postprocess --input {complete_csv} --redistricting_input {input_csv} --output {baf_csv}"
    os.system(command)


def get_centroids_file(points_csv: str, assign_csv: str, centroids_csv: str) -> None:
    """Get sites (district centroids) from assignments

    python3 redistricting.py centroids --points point.csv  --assignment balzer.csv --centroids centroids.csv

    TODO - Todd: Does this still work?
    """

    command: str = f"python3 {dccvt_py}/redistricting.py centroids --points {points_csv}  --assignment {assign_csv} --centroids {centroids_csv}"
    os.system(command)


def combine_centroids_files(inputs: str, output: str) -> None:
    """Concatenate all BG centroids.csv into one file

    cat NC20C_bg_*_centroids.csv > NC20C_block_sites.csv
    """

    command: str = f"cat {inputs} > {output}"
    os.system(command)


### HELPER FUNCTIONS ###


def full_path(dirs: list[str], file_parts: list[str], ext: str = "csv") -> str:
    """Return a fully qualifed file name from a list of directories and a list of file parts"""

    rel_path: str = path_to_file(dirs) + file_name(file_parts, "_", ext)
    return FileSpec(rel_path).abs_path


def label_map(xx: str, plan_type: str) -> str:
    return f"{xx}{cycle[2:]}{plan_type.upper()[0]}"


def label_iteration(I: int, K: int, N: int) -> str:
    return f"I{I:03d}K{K:02d}N{N:02d}"


### END ###
