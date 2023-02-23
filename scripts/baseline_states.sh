#!/bin/bash
#
# Pre-process data for states
#
# For example:
#
# scripts/baseline_states.sh
#
# TODO
# - BGs: CA, OR
# - Fail: MN, NV, NY, TN, WA
#

echo "Generating baseline districts for AL / 2020 / congress..."
scripts/baseline_state.py AL congress -v > logs/AL_2020_congress_log.txt

echo "Generating baseline districts for AZ / 2020 / congress..."
scripts/baseline_state.py AZ congress -v > logs/AZ_2020_congress_log.txt

echo "Generating baseline districts for AR / 2020 / congress..."
scripts/baseline_state.py AR congress -v > logs/AR_2020_congress_log.txt

# TODO - Modify BG strategy
# echo "Generating baseline districts for CA / 2020 / congress..."
# scripts/baseline_state.py CA congress -g -v > logs/CA_2020_congress_log.txt

echo "Generating baseline districts for CO / 2020 / congress..."
scripts/baseline_state.py CO congress -v > logs/CO_2020_congress_log.txt

echo "Generating baseline districts for CT / 2020 / congress..."
scripts/baseline_state.py CT congress -v > logs/CT_2020_congress_log.txt

echo "Generating baseline districts for FL / 2020 / congress..."
scripts/baseline_state.py FL congress -v > logs/FL_2020_congress_log.txt

echo "Generating baseline districts for GA / 2020 / congress..."
scripts/baseline_state.py GA congress -v > logs/GA_2020_congress_log.txt

echo "Generating baseline districts for IL / 2020 / congress..."
scripts/baseline_state.py IL congress -v > logs/IL_2020_congress_log.txt

echo "Generating baseline districts for IN / 2020 / congress..."
scripts/baseline_state.py IN congress -v > logs/IN_2020_congress_log.txt

echo "Generating baseline districts for IA / 2020 / congress..."
scripts/baseline_state.py IA congress -v > logs/IA_2020_congress_log.txt

echo "Generating baseline districts for KS / 2020 / congress..."
scripts/baseline_state.py KS congress -v > logs/KS_2020_congress_log.txt

echo "Generating baseline districts for KY / 2020 / congress..."
scripts/baseline_state.py KY congress -v > logs/KY_2020_congress_log.txt

echo "Generating baseline districts for LA / 2020 / congress..."
scripts/baseline_state.py LA congress -v > logs/LA_2020_congress_log.txt

# echo "Generating baseline districts for MD / 2020 / congress..."
# scripts/baseline_state.py MD congress -v > logs/MD_2020_congress_log.txt

echo "Generating baseline districts for MA / 2020 / congress..."
scripts/baseline_state.py MA congress -v > logs/MA_2020_congress_log.txt

echo "Generating baseline districts for MI / 2020 / congress..."
scripts/baseline_state.py MI congress -v > logs/MI_2020_congress_log.txt

echo "Generating baseline districts for MN / 2020 / congress..."
scripts/baseline_state.py MN congress -v > logs/MN_2020_congress_log.txt

echo "Generating baseline districts for MS / 2020 / congress..."
scripts/baseline_state.py MS congress -v > logs/MS_2020_congress_log.txt

echo "Generating baseline districts for MO / 2020 / congress..."
scripts/baseline_state.py MO congress -v > logs/MO_2020_congress_log.txt

echo "Generating baseline districts for NE / 2020 / congress..."
scripts/baseline_state.py NE congress -v > logs/NE_2020_congress_log.txt

echo "Generating baseline districts for NV / 2020 / congress..."
scripts/baseline_state.py NV congress -v > logs/NV_2020_congress_log.txt

echo "Generating baseline districts for NJ / 2020 / congress..."
scripts/baseline_state.py NJ congress -v > logs/NJ_2020_congress_log.txt

echo "Generating baseline districts for NM / 2020 / congress..."
scripts/baseline_state.py NM congress -v > logs/NM_2020_congress_log.txt

echo "Generating baseline districts for NY / 2020 / congress..."
scripts/baseline_state.py NY congress -v > logs/NY_2020_congress_log.txt

# echo "Generating baseline districts for NC / 2020 / congress..."
# scripts/baseline_state.py NC congress -v > logs/NC_2020_congress_log.txt

echo "Generating baseline districts for OH / 2020 / congress..."
scripts/baseline_state.py OH congress -v > logs/OH_2020_congress_log.txt

echo "Generating baseline districts for OK / 2020 / congress..."
scripts/baseline_state.py OK congress -v > logs/OK_2020_congress_log.txt

# TODO - Modify BG strategy
# echo "Generating baseline districts for OR / 2020 / congress..."
# scripts/baseline_state.py OR congress -g -v > logs/OR_2020_congress_log.txt

# echo "Generating baseline districts for PA / 2020 / congress..."
# scripts/baseline_state.py PA congress -v > logs/PA_2020_congress_log.txt

echo "Generating baseline districts for SC / 2020 / congress..."
scripts/baseline_state.py SC congress -v > logs/SC_2020_congress_log.txt

echo "Generating baseline districts for TN / 2020 / congress..."
scripts/baseline_state.py TN congress -v > logs/TN_2020_congress_log.txt

echo "Generating baseline districts for TX / 2020 / congress..."
scripts/baseline_state.py TX congress -v > logs/TX_2020_congress_log.txt

echo "Generating baseline districts for UT / 2020 / congress..."
scripts/baseline_state.py UT congress -v > logs/UT_2020_congress_log.txt

# echo "Generating baseline districts for VA / 2020 / congress..."
# scripts/baseline_state.py VA congress -v > logs/VA_2020_congress_log.txt

echo "Generating baseline districts for WA / 2020 / congress..."
scripts/baseline_state.py WA congress -v > logs/WA_2020_congress_log.txt

echo "Generating baseline districts for WI / 2020 / congress..."
scripts/baseline_state.py WI congress -v > logs/WI_2020_congress_log.txt

echo "... done."