#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for AL ..."
scripts/extract_pop.py AL > data/AL/AL_census_log.txt
scripts/extract_xy.py AL
scripts/join_feature_data.py AL
scripts/unpickle_to_csv.py AL block

# echo "Processing data for MD ..."
# scripts/extract_pop.py MD > data/MD/MD_census_log.txt
# scripts/extract_xy.py MD
# scripts/join_feature_data.py MD
# scripts/unpickle_to_csv.py MD block
# # scripts/unpickle_to_csv.py MD tract
# # scripts/unpickle_to_csv.py MD bg
