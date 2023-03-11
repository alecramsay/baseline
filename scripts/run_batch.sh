#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

scripts/extract_data.py -s NC
scripts/extract_data.py -s MD
scripts/extract_data.py -s PA
scripts/extract_data.py -s VA

scripts/extract_pop.py -s FL -p -i 3 > data/FL/FL_census_log.txt
scripts/extract_xy.py -s FL -p
scripts/join_feature_data.py -s FL -p
scripts/unpickle_to_csv.py -s FL -u vtd

