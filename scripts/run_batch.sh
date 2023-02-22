#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for VA ..."
scripts/extract_pop.py -s VA -p -i 3 > data/VA/VA_census_log.txt
scripts/extract_xy.py -s VA -p
scripts/join_feature_data.py -s VA -p
scripts/unpickle_to_csv.py -s VA -u vtd
# scripts/unpickle_to_csv.py VA block
# scripts/unpickle_to_csv.py VA bg
