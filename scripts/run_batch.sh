#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for NC ..."
scripts/extract_pop.py NC > data/NC/NC_census_log.txt
scripts/extract_xy.py NC
scripts/join_feature_data.py NC
scripts/unpickle_to_csv.py NC tract
scripts/unpickle_to_csv.py NC bg
scripts/unpickle_to_csv.py NC block

