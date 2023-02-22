#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for MD ..."
scripts/extract_pop.py -s MD -p -i 3 > data/MD/MD_census_log.txt
scripts/extract_xy.py -s MD -p
scripts/join_feature_data.py -s MD -p
scripts/unpickle_to_csv.py -s MD -u vtd
# scripts/unpickle_to_csv.py MD block
# scripts/unpickle_to_csv.py MD bg
