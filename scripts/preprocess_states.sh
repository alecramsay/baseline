#!/bin/bash
#
# Pre-process data for states
#
# For example:
#
# scripts/preprocess_states.sh
#

# echo "Processing data for AK ..."
# scripts/extract_pop.py AK > data/AK/AK_census_log.txt
# scripts/extract_xy.py AK
# scripts/join_feature_data.py AK
# scripts/unpickle_to_csv.py AK block
# # scripts/unpickle_to_csv.py AK tract
# # scripts/unpickle_to_csv.py AK bg

echo "Processing data for AL ..."
scripts/extract_pop.py AL > data/AL/AL_census_log.txt
scripts/extract_xy.py AL
scripts/join_feature_data.py AL
scripts/unpickle_to_csv.py AL block
# scripts/unpickle_to_csv.py AL tract
# scripts/unpickle_to_csv.py AL bg

echo "Processing data for AR ..."
scripts/extract_pop.py AR > data/AR/AR_census_log.txt
scripts/extract_xy.py AR
scripts/join_feature_data.py AR
scripts/unpickle_to_csv.py AR block
# scripts/unpickle_to_csv.py AR tract
# scripts/unpickle_to_csv.py AR bg

echo "Processing data for AZ ..."
scripts/extract_pop.py AZ > data/AZ/AZ_census_log.txt
scripts/extract_xy.py AZ
scripts/join_feature_data.py AZ
scripts/unpickle_to_csv.py AZ block
# scripts/unpickle_to_csv.py AZ tract
# scripts/unpickle_to_csv.py AZ bg

echo "Processing data for CA ..."
scripts/extract_pop.py CA > data/CA/CA_census_log.txt
scripts/extract_xy.py CA
scripts/join_feature_data.py CA
scripts/unpickle_to_csv.py CA block
# scripts/unpickle_to_csv.py CA tract
# scripts/unpickle_to_csv.py CA bg

echo "Processing data for CO ..."
scripts/extract_pop.py CO > data/CO/CO_census_log.txt
scripts/extract_xy.py CO
scripts/join_feature_data.py CO
scripts/unpickle_to_csv.py CO block
# scripts/unpickle_to_csv.py CO tract
# scripts/unpickle_to_csv.py CO bg

echo "Processing data for CT ..."
scripts/extract_pop.py CT > data/CT/CT_census_log.txt
scripts/extract_xy.py CT
scripts/join_feature_data.py CT
scripts/unpickle_to_csv.py CT block
# scripts/unpickle_to_csv.py CT tract
# scripts/unpickle_to_csv.py CT bg

# echo "Processing data for DE ..."
# scripts/extract_pop.py DE > data/DE/DE_census_log.txt
# scripts/extract_xy.py DE
# scripts/join_feature_data.py DE
# scripts/unpickle_to_csv.py DE block
# # scripts/unpickle_to_csv.py DE tract
# # scripts/unpickle_to_csv.py DE bg

echo "Processing data for FL ..."
scripts/extract_pop.py FL > data/FL/FL_census_log.txt
scripts/extract_xy.py FL
scripts/join_feature_data.py FL
scripts/unpickle_to_csv.py FL block
# scripts/unpickle_to_csv.py FL tract
# scripts/unpickle_to_csv.py FL bg

echo "Processing data for GA ..."
scripts/extract_pop.py GA > data/GA/GA_census_log.txt
scripts/extract_xy.py GA
scripts/join_feature_data.py GA
scripts/unpickle_to_csv.py GA block
# scripts/unpickle_to_csv.py GA tract
# scripts/unpickle_to_csv.py GA bg

# echo "Processing data for HI ..."
# scripts/extract_pop.py HI > data/HI/HI_census_log.txt
# scripts/extract_xy.py HI
# scripts/join_feature_data.py HI
# scripts/unpickle_to_csv.py HI block
# # scripts/unpickle_to_csv.py HI tract
# # scripts/unpickle_to_csv.py HI bg

echo "Processing data for IA ..."
scripts/extract_pop.py IA > data/IA/IA_census_log.txt
scripts/extract_xy.py IA
scripts/join_feature_data.py IA
scripts/unpickle_to_csv.py IA block
# scripts/unpickle_to_csv.py IA tract
# scripts/unpickle_to_csv.py IA bg

# echo "Processing data for ID ..."
# scripts/extract_pop.py ID > data/ID/ID_census_log.txt
# scripts/extract_xy.py ID
# scripts/join_feature_data.py ID
# scripts/unpickle_to_csv.py ID block
# # scripts/unpickle_to_csv.py ID tract
# # scripts/unpickle_to_csv.py ID bg

echo "Processing data for IL ..."
scripts/extract_pop.py IL > data/IL/IL_census_log.txt
scripts/extract_xy.py IL
scripts/join_feature_data.py IL
scripts/unpickle_to_csv.py IL block
# scripts/unpickle_to_csv.py IL tract
# scripts/unpickle_to_csv.py IL bg

echo "Processing data for IN ..."
scripts/extract_pop.py IN > data/IN/IN_census_log.txt
scripts/extract_xy.py IN
scripts/join_feature_data.py IN
scripts/unpickle_to_csv.py IN block
# scripts/unpickle_to_csv.py IN tract
# scripts/unpickle_to_csv.py IN bg

echo "Processing data for KS ..."
scripts/extract_pop.py KS > data/KS/KS_census_log.txt
scripts/extract_xy.py KS
scripts/join_feature_data.py KS
scripts/unpickle_to_csv.py KS block
# scripts/unpickle_to_csv.py KS tract
# scripts/unpickle_to_csv.py KS bg

echo "Processing data for KY ..."
scripts/extract_pop.py KY > data/KY/KY_census_log.txt
scripts/extract_xy.py KY
scripts/join_feature_data.py KY
scripts/unpickle_to_csv.py KY block
# scripts/unpickle_to_csv.py KY tract
# scripts/unpickle_to_csv.py KY bg

echo "Processing data for LA ..."
scripts/extract_pop.py LA > data/LA/LA_census_log.txt
scripts/extract_xy.py LA
scripts/join_feature_data.py LA
scripts/unpickle_to_csv.py LA block
# scripts/unpickle_to_csv.py LA tract
# scripts/unpickle_to_csv.py LA bg

echo "Processing data for MA ..."
scripts/extract_pop.py MA > data/MA/MA_census_log.txt
scripts/extract_xy.py MA
scripts/join_feature_data.py MA
scripts/unpickle_to_csv.py MA block
# scripts/unpickle_to_csv.py MA tract
# scripts/unpickle_to_csv.py MA bg

echo "Processing data for MD ..."
scripts/extract_pop.py MD > data/MD/MD_census_log.txt
scripts/extract_xy.py MD
scripts/join_feature_data.py MD
scripts/unpickle_to_csv.py MD block
# scripts/unpickle_to_csv.py MD tract
# scripts/unpickle_to_csv.py MD bg

# echo "Processing data for ME ..."
# scripts/extract_pop.py ME > data/ME/ME_census_log.txt
# scripts/extract_xy.py ME
# scripts/join_feature_data.py ME
# scripts/unpickle_to_csv.py ME block
# # scripts/unpickle_to_csv.py ME tract
# # scripts/unpickle_to_csv.py ME bg

echo "Processing data for MI ..."
scripts/extract_pop.py MI > data/MI/MI_census_log.txt
scripts/extract_xy.py MI
scripts/join_feature_data.py MI
scripts/unpickle_to_csv.py MI block
# scripts/unpickle_to_csv.py MI tract
# scripts/unpickle_to_csv.py MI bg

echo "Processing data for MN ..."
scripts/extract_pop.py MN > data/MN/MN_census_log.txt
scripts/extract_xy.py MN
scripts/join_feature_data.py MN
scripts/unpickle_to_csv.py MN block
# scripts/unpickle_to_csv.py MN tract
# scripts/unpickle_to_csv.py MN bg

echo "Processing data for MO ..."
scripts/extract_pop.py MO > data/MO/MO_census_log.txt
scripts/extract_xy.py MO
scripts/join_feature_data.py MO
scripts/unpickle_to_csv.py MO block
# scripts/unpickle_to_csv.py MO tract
# scripts/unpickle_to_csv.py MO bg

echo "Processing data for MS ..."
scripts/extract_pop.py MS > data/MS/MS_census_log.txt
scripts/extract_xy.py MS
scripts/join_feature_data.py MS
scripts/unpickle_to_csv.py MS block
# scripts/unpickle_to_csv.py MS tract
# scripts/unpickle_to_csv.py MS bg

# echo "Processing data for MT ..."
# scripts/extract_pop.py MT > data/MT/MT_census_log.txt
# scripts/extract_xy.py MT
# scripts/join_feature_data.py MT
# scripts/unpickle_to_csv.py MT block
# # scripts/unpickle_to_csv.py MT tract
# # scripts/unpickle_to_csv.py MT bg

echo "Processing data for NC ..."
scripts/extract_pop.py NC > data/NC/NC_census_log.txt
scripts/extract_xy.py NC
scripts/join_feature_data.py NC
scripts/unpickle_to_csv.py NC block
# # scripts/unpickle_to_csv.py NC tract
# # scripts/unpickle_to_csv.py NC bg

# echo "Processing data for ND ..."
# scripts/extract_pop.py ND > data/ND/ND_census_log.txt
# scripts/extract_xy.py ND
# scripts/join_feature_data.py ND
# scripts/unpickle_to_csv.py ND block
# # scripts/unpickle_to_csv.py ND tract
# # scripts/unpickle_to_csv.py ND bg

echo "Processing data for NE ..."
scripts/extract_pop.py NE > data/NE/NE_census_log.txt
scripts/extract_xy.py NE
scripts/join_feature_data.py NE
scripts/unpickle_to_csv.py NE block
# scripts/unpickle_to_csv.py NE tract
# scripts/unpickle_to_csv.py NE bg

# echo "Processing data for NH ..."
# scripts/extract_pop.py NH > data/NH/NH_census_log.txt
# scripts/extract_xy.py NH
# scripts/join_feature_data.py NH
# scripts/unpickle_to_csv.py NH block
# # scripts/unpickle_to_csv.py NH tract
# # scripts/unpickle_to_csv.py NH bg

echo "Processing data for NJ ..."
scripts/extract_pop.py NJ > data/NJ/NJ_census_log.txt
scripts/extract_xy.py NJ
scripts/join_feature_data.py NJ
scripts/unpickle_to_csv.py NJ block
# scripts/unpickle_to_csv.py NJ tract
# scripts/unpickle_to_csv.py NJ bg

echo "Processing data for NM ..."
scripts/extract_pop.py NM > data/NM/NM_census_log.txt
scripts/extract_xy.py NM
scripts/join_feature_data.py NM
scripts/unpickle_to_csv.py NM block
# scripts/unpickle_to_csv.py NM tract
# scripts/unpickle_to_csv.py NM bg

echo "Processing data for NV ..."
scripts/extract_pop.py NV > data/NV/NV_census_log.txt
scripts/extract_xy.py NV
scripts/join_feature_data.py NV
scripts/unpickle_to_csv.py NV block
# scripts/unpickle_to_csv.py NV tract
# scripts/unpickle_to_csv.py NV bg

echo "Processing data for NY ..."
scripts/extract_pop.py NY > data/NY/NY_census_log.txt
scripts/extract_xy.py NY
scripts/join_feature_data.py NY
scripts/unpickle_to_csv.py NY block
# scripts/unpickle_to_csv.py NY tract
# scripts/unpickle_to_csv.py NY bg

echo "Processing data for OH ..."
scripts/extract_pop.py OH > data/OH/OH_census_log.txt
scripts/extract_xy.py OH
scripts/join_feature_data.py OH
scripts/unpickle_to_csv.py OH block
# scripts/unpickle_to_csv.py OH tract
# scripts/unpickle_to_csv.py OH bg

echo "Processing data for OK ..."
scripts/extract_pop.py OK > data/OK/OK_census_log.txt
scripts/extract_xy.py OK
scripts/join_feature_data.py OK
scripts/unpickle_to_csv.py OK block
# scripts/unpickle_to_csv.py OK tract
# scripts/unpickle_to_csv.py OK bg

echo "Processing data for OR ..."
scripts/extract_pop.py OR > data/OR/OR_census_log.txt
scripts/extract_xy.py OR
scripts/join_feature_data.py OR
scripts/unpickle_to_csv.py OR block
# scripts/unpickle_to_csv.py OR tract
# scripts/unpickle_to_csv.py OR bg

echo "Processing data for PA ..."
scripts/extract_pop.py PA > data/PA/PA_census_log.txt
scripts/extract_xy.py PA
scripts/join_feature_data.py PA
scripts/unpickle_to_csv.py PA block
# scripts/unpickle_to_csv.py PA tract
# scripts/unpickle_to_csv.py PA bg

# echo "Processing data for RI ..."
# scripts/extract_pop.py RI > data/RI/RI_census_log.txt
# scripts/extract_xy.py RI
# scripts/join_feature_data.py RI
# scripts/unpickle_to_csv.py RI block
# # scripts/unpickle_to_csv.py RI tract
# # scripts/unpickle_to_csv.py RI bg

echo "Processing data for SC ..."
scripts/extract_pop.py SC > data/SC/SC_census_log.txt
scripts/extract_xy.py SC
scripts/join_feature_data.py SC
scripts/unpickle_to_csv.py SC block
# scripts/unpickle_to_csv.py SC tract
# scripts/unpickle_to_csv.py SC bg

# echo "Processing data for SD ..."
# scripts/extract_pop.py SD > data/SD/SD_census_log.txt
# scripts/extract_xy.py SD
# scripts/join_feature_data.py SD
# scripts/unpickle_to_csv.py SD block
# # scripts/unpickle_to_csv.py SD tract
# # scripts/unpickle_to_csv.py SD bg

echo "Processing data for TN ..."
scripts/extract_pop.py TN > data/TN/TN_census_log.txt
scripts/extract_xy.py TN
scripts/join_feature_data.py TN
scripts/unpickle_to_csv.py TN block
# scripts/unpickle_to_csv.py TN tract
# scripts/unpickle_to_csv.py TN bg

echo "Processing data for TX ..."
scripts/extract_pop.py TX > data/TX/TX_census_log.txt
scripts/extract_xy.py TX
scripts/join_feature_data.py TX
scripts/unpickle_to_csv.py TX block
# scripts/unpickle_to_csv.py TX tract
# scripts/unpickle_to_csv.py TX bg

echo "Processing data for UT ..."
scripts/extract_pop.py UT > data/UT/UT_census_log.txt
scripts/extract_xy.py UT
scripts/join_feature_data.py UT
scripts/unpickle_to_csv.py UT block
# scripts/unpickle_to_csv.py UT tract
# scripts/unpickle_to_csv.py UT bg

echo "Processing data for VA ..."
scripts/extract_pop.py VA > data/VA/VA_census_log.txt
scripts/extract_xy.py VA
scripts/join_feature_data.py VA
scripts/unpickle_to_csv.py VA block
# scripts/unpickle_to_csv.py VA tract
# scripts/unpickle_to_csv.py VA bg

# echo "Processing data for VT ..."
# scripts/extract_pop.py VT > data/VT/VT_census_log.txt
# scripts/extract_xy.py VT
# scripts/join_feature_data.py VT
# scripts/unpickle_to_csv.py VT block
# # scripts/unpickle_to_csv.py VT tract
# # scripts/unpickle_to_csv.py VT bg

echo "Processing data for WA ..."
scripts/extract_pop.py WA > data/WA/WA_census_log.txt
scripts/extract_xy.py WA
scripts/join_feature_data.py WA
scripts/unpickle_to_csv.py WA block
# scripts/unpickle_to_csv.py WA tract
# scripts/unpickle_to_csv.py WA bg

echo "Processing data for WI ..."
scripts/extract_pop.py WI > data/WI/WI_census_log.txt
scripts/extract_xy.py WI
scripts/join_feature_data.py WI
scripts/unpickle_to_csv.py WI block
# scripts/unpickle_to_csv.py WI tract
# scripts/unpickle_to_csv.py WI bg

# echo "Processing data for WV ..."
# scripts/extract_pop.py WV > data/WV/WV_census_log.txt
# scripts/extract_xy.py WV
# scripts/join_feature_data.py WV
# scripts/unpickle_to_csv.py WV block
# # scripts/unpickle_to_csv.py WV tract
# # scripts/unpickle_to_csv.py WV bg

# echo "Processing data for WY ..."
# scripts/extract_pop.py WY > data/WY/WY_census_log.txt
# scripts/extract_xy.py WY
# scripts/join_feature_data.py WY
# scripts/unpickle_to_csv.py WY
# # scripts/unpickle_to_csv.py WY tract
# # scripts/unpickle_to_csv.py WY bg