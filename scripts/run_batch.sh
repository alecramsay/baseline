#!/bin/bash
#
# Run multiple scripts
#
# For example:
#
# scripts/run_batch.sh
#

scripts/preprocess_state.py -s NC
scripts/preprocess_state.py -s MD
scripts/preprocess_state.py -s PA
scripts/preprocess_state.py -s VA
