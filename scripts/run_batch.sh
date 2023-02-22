#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for NC ..."
scripts/extract_pop.py -s NC -p -i 3 > data/NC/NC_census_log.txt
scripts/extract_xy.py -s NC -p
scripts/join_feature_data.py -s NC -p
scripts/unpickle_to_csv.py -s NC -u vtd
# scripts/unpickle_to_csv.py NC block
# scripts/unpickle_to_csv.py NC bg
