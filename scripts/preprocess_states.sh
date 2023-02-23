#!/bin/bash
#
# Pre-process data for states
#
# For example:
#
# scripts/preprocess_states.sh
#

echo "Preprocessing data for AL ..."
scripts/preprocess_state.py -s AL

echo "Preprocessing data for AZ ..."
scripts/preprocess_state.py -s AZ

echo "Preprocessing data for AR ..."
scripts/preprocess_state.py -s AR

# CA uses BG's instead of VTD's
echo "Preprocessing data for CA ..."
scripts/extract_pop.py -s CA -g -i 3 > data/CA/CA_census_log.txt
scripts/extract_xy.py -s CA -g
scripts/join_feature_data.py -s CA -g
scripts/unpickle_to_csv.py -s CA -u bg

echo "Preprocessing data for CO ..."
scripts/preprocess_state.py -s CO

echo "Preprocessing data for CT ..."
scripts/preprocess_state.py -s CT

echo "Preprocessing data for FL ..."
scripts/preprocess_state.py -s FL

echo "Preprocessing data for GA ..."
scripts/preprocess_state.py -s GA

echo "Preprocessing data for IL ..."
scripts/preprocess_state.py -s IL

echo "Preprocessing data for IN ..."
scripts/preprocess_state.py -s IN

echo "Preprocessing data for IA ..."
scripts/preprocess_state.py -s IA

echo "Preprocessing data for KS ..."
scripts/preprocess_state.py -s KS

echo "Preprocessing data for KY ..."
scripts/preprocess_state.py -s KY

echo "Preprocessing data for LA ..."
scripts/preprocess_state.py -s LA

echo "Preprocessing data for MD ..."
scripts/preprocess_state.py -s MD

echo "Preprocessing data for MA ..."
scripts/preprocess_state.py -s MA

echo "Preprocessing data for MI ..."
scripts/preprocess_state.py -s MI

echo "Preprocessing data for MN ..."
scripts/preprocess_state.py -s MN

echo "Preprocessing data for MS ..."
scripts/preprocess_state.py -s MS

echo "Preprocessing data for MO ..."
scripts/preprocess_state.py -s MO

echo "Preprocessing data for NE ..."
scripts/preprocess_state.py -s NE

echo "Preprocessing data for NV ..."
scripts/preprocess_state.py -s NV

echo "Preprocessing data for NJ ..."
scripts/preprocess_state.py -s NJ

echo "Preprocessing data for NM ..."
scripts/preprocess_state.py -s NM

echo "Preprocessing data for NY ..."
scripts/preprocess_state.py -s NY

echo "Preprocessing data for NC ..."
scripts/preprocess_state.py -s NC

echo "Preprocessing data for OH ..."
scripts/preprocess_state.py -s OH

echo "Preprocessing data for OK ..."
scripts/preprocess_state.py -s OK

echo "Preprocessing data for OR ..."
scripts/extract_pop.py -s OR -g -i 3 > data/OR/OR_census_log.txt
scripts/extract_xy.py -s OR -g
scripts/join_feature_data.py -s OR -g
scripts/unpickle_to_csv.py -s OR -u bg

echo "Preprocessing data for PA ..."
scripts/preprocess_state.py -s PA

echo "Preprocessing data for SC ..."
scripts/preprocess_state.py -s SC

echo "Preprocessing data for TN ..."
scripts/preprocess_state.py -s TN

echo "Preprocessing data for TX ..."
scripts/preprocess_state.py -s TX

echo "Preprocessing data for UT ..."
scripts/preprocess_state.py -s UT

echo "Preprocessing data for VA ..."
scripts/preprocess_state.py -s VA

echo "Preprocessing data for WA ..."
scripts/preprocess_state.py -s WA

echo "Preprocessing data for WI ..."
scripts/preprocess_state.py -s WI

echo "... done."