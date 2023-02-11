#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

echo "Processing data for AL ..."
scripts/extract_pop.py -g AL > data/AL/AL_census_log.txt
scripts/extract_xy.py -g AL
scripts/join_feature_data.py -g AL
scripts/unpickle_to_csv.py AL block
# scripts/unpickle_to_csv.py AL tract
scripts/unpickle_to_csv.py AL bg
