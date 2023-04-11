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
    """Create a baseline candidate map by calling dccvt/examples/redistricting/create.sh.

    Do this many times, and then choose the baseline as the map with the lowest energy.

    TODO - Rename this and integrate it into create_baseline_candidate.
    """

    command: str = f"create.sh --tmpdir={tmpdir} --N={N} --seed={seed} --prefix={prefix} --data={data} --adjacencies={adjacencies} --output={output} --label={label}"
    os.system(command)


def create_baseline_candidate(
    *,
    tmpdir: str,
    N: int,
    seed: int,
    prefix: str,
    data: str,
    adjacencies: str,
    label: str,
    output: str,
    verbose: bool = False,
) -> None:
    """Create a baseline candidate map by emulating dccvt/examples/redistricting/create.sh w/ individual dccvt wrappers calls.

    Do this many times, and then choose the baseline as the map with the lowest energy.
    """

    THRESHOLD: int = 1000

    if verbose:
        print(f"Generate candidate baseline map:")
        print(f"- tmpdir: {tmpdir}")
        print(f"- N: {N}")
        print(f"- seed: {seed}")
        print(f"- prefix: {prefix}")
        print(f"- data: {data}")
        print(f"- adjacencies: {adjacencies}")
        print(f"- label: {label}")
        print(f"- output: {output}")
        print()

    data_csv: str = data
    adjacencies_csv: str = adjacencies
    output_csv: str = output

    points_csv: str = f"{tmpdir}/{prefix}.points.csv"
    sites_csv: str = f"{tmpdir}/{prefix}.randomsites.csv"
    initial_csv: str = f"{tmpdir}/{prefix}.initialized.csv"  # balanced, noncontiguous
    balzer_1_csv: str = (
        f"{tmpdir}/{prefix}.balzer.csv"  # initial, balanced, noncontiguous
    )
    unbalanced_csv: str = f"{tmpdir}/{prefix}.unbalancedcontiguous.csv"
    balzer_2_csv: str = (
        f"{tmpdir}/{prefix}.balzerunbalancedcontiguous.csv"  # unbalanced, contiguous
    )
    balanced_csv: str = f"{tmpdir}/{prefix}.balancedcontiguous.csv"
    balzer_3_csv: str = (
        f"{tmpdir}/{prefix}.balzerbalancedcontiguous.csv"  # balanced, contiguous
    )
    consolidated_csv: str = f"{tmpdir}/{prefix}.consolidated.csv"
    complete_csv: str = f"{tmpdir}/{prefix}.complete.csv"

    if verbose:
        print(f"- points_csv: {points_csv}")
        print(f"- sites_csv: {sites_csv}")
        print(f"- initial_csv: {initial_csv}")
        print(f"- balzer_1_csv: {balzer_1_csv}")
        print(f"- unbalanced_csv: {unbalanced_csv}")
        print(f"- balzer_2_csv: {balzer_2_csv}")
        print(f"- balanced_csv: {balanced_csv}")
        print(f"- balzer_3_csv: {balzer_3_csv}")
        print(f"- consolidated_csv: {consolidated_csv}")
        print(f"- complete_csv: {complete_csv}")
        print()

    create_points_file(input_csv=data_csv, output_csv=points_csv, debug=verbose)
    create_random_sites_file(
        points_csv=points_csv, output_csv=sites_csv, seed=seed, n=N, debug=verbose
    )
    create_initial_assignment_file(
        points_csv=points_csv, sites_csv=sites_csv, output_csv=initial_csv
    )
    run_balzer(
        points_csv=points_csv,
        initial_csv=initial_csv,
        adjacencies_csv=adjacencies_csv,
        threshold=THRESHOLD,
        output_csv=balzer_1_csv,
        debug=verbose,
    )  # Create initial, balanced, noncontiguous balzer file
    create_unbalanced_contiguous_assignment_file(
        assignment_csv=balzer_1_csv,
        adjacencies_csv=adjacencies_csv,
        output_csv=unbalanced_csv,
        debug=verbose,
    )
    run_balzer(
        points_csv=points_csv,
        initial_csv=unbalanced_csv,
        adjacencies_csv=adjacencies_csv,
        threshold=THRESHOLD,
        output_csv=balzer_2_csv,
        debug=verbose,
    )  # Create unbalanced, contiguous, balzer file
    create_balanced_contiguous_assignment_file(
        assignment_csv=unbalanced_csv,
        adjacencies_csv=adjacencies_csv,
        max_iterations=1000,
        output_csv=balanced_csv,
        debug=verbose,
    )
    run_balzer(
        points_csv=points_csv,
        initial_csv=balanced_csv,
        adjacencies_csv=adjacencies_csv,
        threshold=THRESHOLD,
        output_csv=balzer_3_csv,
        debug=verbose,
    )  # Create balanced, contiguous, balzer file

    create_consolidated_file(
        assignment_csv=balzer_3_csv,
        adjacencies_csv=adjacencies_csv,
        label=label,
        output_csv=consolidated_csv,
        debug=verbose,
    )
    # TODO - HERE
    print()
    print("More ...")

    pass


### DCCVT WRAPPERS ###


def create_points_file(*, input_csv: str, output_csv: str, debug: bool = False) -> None:
    """Create points.csv from preferred redistricting input.csv format

    python3 geoid.py points --input redistricting.csv --output points.csv
    """

    command: str = (
        f"python3 {dccvt_py}/geoid.py points --input {input_csv} --output {output_csv}"
    )
    execute(command, debug)


def create_random_sites_file(
    *, points_csv: str, output_csv: str, seed: int, n: int, debug: bool = False
) -> None:
    """Create random sites from points.csv

    python3 redistricting.py sites --points points.csv --output sites.csv --seed 31415 --N 14
    """

    command: str = f"python3 {dccvt_py}/redistricting.py sites --points {points_csv} --output {output_csv} --seed {seed} --N {n}"
    execute(command, debug)


def create_initial_assignment_file(
    *, points_csv: str, sites_csv: str, output_csv: str, debug: bool = False
) -> None:
    """Create starting sites from points.csv

    python3 redistricting.py initial --sites sites.csv --points points.csv --output initial.csv
    """

    command: str = f"python3 {dccvt_py}/redistricting.py initial --points {points_csv} --sites {sites_csv} --output {output_csv}"
    execute(command, debug)


def run_balzer(
    *,
    points_csv: str,
    initial_csv: str,
    adjacencies_csv: str,
    threshold: int,
    output_csv: str,
    debug: bool = False,
) -> None:
    """Run Balzer

    ../../bin/dccvt --sites sites.csv --points points.csv --initial initial.csv --threshold threshold --output balzer.csv
    """

    command: str = f"{dccvt_go}/dccvt --points {points_csv} --initial {initial_csv} --adjacencies {adjacencies_csv} --threshold {threshold} --output {output_csv}"
    execute(command, debug)


def create_unbalanced_contiguous_assignment_file(
    *, assignment_csv: str, adjacencies_csv: str, output_csv: str, debug: bool = False
) -> None:
    """Create an unbalanced contiguous assignment file

    python3 redistricting.py contiguous \
        --assignment "$balzer_balanced_noncontiguous_assignmentfile" \
        --adjacent "$adjacenciesfile" \
        --output "$unbalanced_contiguous_assignmentfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py contiguous --assignment {assignment_csv} --adjacent {adjacencies_csv} --output {output_csv}"
    execute(command, debug)


def create_balanced_contiguous_assignment_file(
    *,
    assignment_csv: str,
    adjacencies_csv: str,
    max_iterations: int,
    output_csv: str,
    debug: bool = False,
) -> None:
    """Create a balanced contiguous assignment file

    python3 redistricting.py rebalance \
        --assignment "$balzer_unbalanced_contiguous_assignmentfile" \
        --adjacent "$adjacenciesfile" \
        --max_iterations 1000 \
        --output "$balanced_contiguous_assignmentfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py rebalance --assignment {assignment_csv} --adjacent {adjacencies_csv} --max_iterations {max_iterations} --output {output_csv}"
    execute(command, debug)


def create_consolidated_file(
    *,
    assignment_csv: str,
    adjacencies_csv: str,
    label: str,
    output_csv: str,
    debug: bool = False,
) -> None:
    """Consolidate potentially fractional/split assignments in balzer.csv to unique assignments in consolidated.csv

    python3 redistricting.py consolidate \
    --assignment "$balzer_balanced_contiguous_assignmentfile" \
    --adjacent "$adjacenciesfile" \
    --label "$label" \
    --output "$consolidatedfile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py consolidate --assignment {assignment_csv} --adjacent {adjacencies_csv} --label {label} --output {output_csv}"
    execute(command, debug)


def create_complete_file(
    consolidated_csv: str,
    adjacencies_csv: str,
    points_csv: str,
    complete_csv: str,
    debug: bool = False,
) -> None:
    """Create complete file

    python3 redistricting.py complete \
        --assignment "$consolidatedfile" \
        --adjacent "$adjacenciesfile" \
        --points "$pointsfile" \
        --output "$completefile"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py complete --assignment {consolidated_csv} --adjacent {adjacencies_csv} --points {points_csv} --output {complete_csv}"
    execute(command, debug)


def compute_energy(
    assignment_csv: str, points_csv: str, label: str, debug: bool = False
) -> None:
    """Computing energy of a completed map

    python3 redistricting.py energy \
        --assignment "$completefile" \
        --points "$pointsfile" \
        --label "$label"
    """

    command: str = f"python3 {dccvt_py}/redistricting.py energy --assignment {assignment_csv} --points {points_csv} --label {label}"
    execute(command, debug)


def create_output_file(
    input_csv: str, complete_csv: str, baf_csv: str, debug: bool = False
) -> None:
    """Make an assignment file from a file of unique assignments of VTDs (or blocks) to districts (sites)

    python3 geoid.py postprocess --input complete.csv --redistricting_input redistricting.csv --output output.csv

    $GEOID postprocess \
    --input "$completefile" \
    --redistricting_input "$infile" \
    --output "$outfile"
    """

    command: str = f"python3 {dccvt_py}/geoid.py postprocess --input {complete_csv} --redistricting_input {input_csv} --output {baf_csv}"
    execute(command, debug)


def get_centroids_file(
    points_csv: str, assign_csv: str, centroids_csv: str, debug: bool = False
) -> None:
    """Get sites (district centroids) from assignments

    python3 redistricting.py centroids --points point.csv  --assignment balzer.csv --centroids centroids.csv

    TODO - Todd: Does this still work?
    """

    command: str = f"python3 {dccvt_py}/redistricting.py centroids --points {points_csv}  --assignment {assign_csv} --centroids {centroids_csv}"
    execute(command, debug)


def combine_centroids_files(inputs: str, output: str, debug: bool = False) -> None:
    """Concatenate all BG centroids.csv into one file

    cat NC20C_bg_*_centroids.csv > NC20C_block_sites.csv
    """

    command: str = f"cat {inputs} > {output}"
    execute(command, debug)


### HELPER FUNCTIONS ###


def execute(command: str, debug: bool = False) -> None:
    """Execute a shell command"""

    if debug:
        print()
        print(command)
    else:
        os.system(command)


def full_path(dirs: list[str], file_parts: list[str], ext: str = "csv") -> str:
    """Return a fully qualifed file name from a list of directories and a list of file parts"""

    rel_path: str = path_to_file(dirs) + file_name(file_parts, "_", ext)
    return FileSpec(rel_path).abs_path


def label_map(xx: str, plan_type: str) -> str:
    return f"{xx}{cycle[2:]}{plan_type.upper()[0]}"


def label_iteration(I: int, K: int, N: int) -> str:
    return f"I{I:03d}K{K:02d}N{N:02d}"


### END ###
