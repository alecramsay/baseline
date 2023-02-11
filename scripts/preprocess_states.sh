#!/bin/bash
#
# Pre-process data for states
#
# For example:
#
# scripts/preprocess_states.sh
#

# echo "Processing data for AK ..."
# scripts/extract_pop.py  -g AK > data/AK/AK_census_log.txt
# scripts/extract_xy.py  -g AK
# scripts/join_feature_data.py -g AK
# scripts/unpickle_to_csv.py AK block
# # scripts/unpickle_to_csv.py AK tract
# scripts/unpickle_to_csv.py AK bg

echo "Processing data for AL ..."
scripts/extract_pop.py  -g AL > data/AL/AL_census_log.txt
scripts/extract_xy.py  -g AL
scripts/join_feature_data.py -g AL
scripts/unpickle_to_csv.py AL block
# scripts/unpickle_to_csv.py AL tract
scripts/unpickle_to_csv.py AL bg

echo "Processing data for AR ..."
scripts/extract_pop.py  -g AR > data/AR/AR_census_log.txt
scripts/extract_xy.py  -g AR
scripts/join_feature_data.py -g AR
scripts/unpickle_to_csv.py AR block
# scripts/unpickle_to_csv.py AR tract
scripts/unpickle_to_csv.py AR bg

echo "Processing data for AZ ..."
scripts/extract_pop.py  -g AZ > data/AZ/AZ_census_log.txt
scripts/extract_xy.py  -g AZ
scripts/join_feature_data.py -g AZ
scripts/unpickle_to_csv.py AZ block
# scripts/unpickle_to_csv.py AZ tract
scripts/unpickle_to_csv.py AZ bg

echo "Processing data for CA ..."
scripts/extract_pop.py  -g CA > data/CA/CA_census_log.txt
scripts/extract_xy.py  -g CA
scripts/join_feature_data.py -g CA
scripts/unpickle_to_csv.py CA block
# scripts/unpickle_to_csv.py CA tract
scripts/unpickle_to_csv.py CA bg

echo "Processing data for CO ..."
scripts/extract_pop.py  -g CO > data/CO/CO_census_log.txt
scripts/extract_xy.py  -g CO
scripts/join_feature_data.py -g CO
scripts/unpickle_to_csv.py CO block
# scripts/unpickle_to_csv.py CO tract
scripts/unpickle_to_csv.py CO bg

echo "Processing data for CT ..."
scripts/extract_pop.py  -g CT > data/CT/CT_census_log.txt
scripts/extract_xy.py  -g CT
scripts/join_feature_data.py -g CT
scripts/unpickle_to_csv.py CT block
# scripts/unpickle_to_csv.py CT tract
scripts/unpickle_to_csv.py CT bg

# echo "Processing data for DE ..."
# scripts/extract_pop.py  -g DE > data/DE/DE_census_log.txt
# scripts/extract_xy.py  -g DE
# scripts/join_feature_data.py -g DE
# scripts/unpickle_to_csv.py DE block
# # scripts/unpickle_to_csv.py DE tract
# scripts/unpickle_to_csv.py DE bg

echo "Processing data for FL ..."
scripts/extract_pop.py  -g FL > data/FL/FL_census_log.txt
scripts/extract_xy.py  -g FL
scripts/join_feature_data.py -g FL
scripts/unpickle_to_csv.py FL block
# scripts/unpickle_to_csv.py FL tract
scripts/unpickle_to_csv.py FL bg

echo "Processing data for GA ..."
scripts/extract_pop.py  -g GA > data/GA/GA_census_log.txt
scripts/extract_xy.py  -g GA
scripts/join_feature_data.py -g GA
scripts/unpickle_to_csv.py GA block
# scripts/unpickle_to_csv.py GA tract
scripts/unpickle_to_csv.py GA bg

# echo "Processing data for HI ..."
# scripts/extract_pop.py  -g HI > data/HI/HI_census_log.txt
# scripts/extract_xy.py  -g HI
# scripts/join_feature_data.py -g HI
# scripts/unpickle_to_csv.py HI block
# # scripts/unpickle_to_csv.py HI tract
# scripts/unpickle_to_csv.py HI bg

echo "Processing data for IA ..."
scripts/extract_pop.py  -g IA > data/IA/IA_census_log.txt
scripts/extract_xy.py  -g IA
scripts/join_feature_data.py -g IA
scripts/unpickle_to_csv.py IA block
# scripts/unpickle_to_csv.py IA tract
scripts/unpickle_to_csv.py IA bg

# echo "Processing data for ID ..."
# scripts/extract_pop.py  -g ID > data/ID/ID_census_log.txt
# scripts/extract_xy.py  -g ID
# scripts/join_feature_data.py -g ID
# scripts/unpickle_to_csv.py ID block
# # scripts/unpickle_to_csv.py ID tract
# scripts/unpickle_to_csv.py ID bg

echo "Processing data for IL ..."
scripts/extract_pop.py  -g IL > data/IL/IL_census_log.txt
scripts/extract_xy.py  -g IL
scripts/join_feature_data.py -g IL
scripts/unpickle_to_csv.py IL block
# scripts/unpickle_to_csv.py IL tract
scripts/unpickle_to_csv.py IL bg

echo "Processing data for IN ..."
scripts/extract_pop.py  -g IN > data/IN/IN_census_log.txt
scripts/extract_xy.py  -g IN
scripts/join_feature_data.py -g IN
scripts/unpickle_to_csv.py IN block
# scripts/unpickle_to_csv.py IN tract
scripts/unpickle_to_csv.py IN bg

echo "Processing data for KS ..."
scripts/extract_pop.py  -g KS > data/KS/KS_census_log.txt
scripts/extract_xy.py  -g KS
scripts/join_feature_data.py -g KS
scripts/unpickle_to_csv.py KS block
# scripts/unpickle_to_csv.py KS tract
scripts/unpickle_to_csv.py KS bg

echo "Processing data for KY ..."
scripts/extract_pop.py  -g KY > data/KY/KY_census_log.txt
scripts/extract_xy.py  -g KY
scripts/join_feature_data.py -g KY
scripts/unpickle_to_csv.py KY block
# scripts/unpickle_to_csv.py KY tract
scripts/unpickle_to_csv.py KY bg

echo "Processing data for LA ..."
scripts/extract_pop.py  -g LA > data/LA/LA_census_log.txt
scripts/extract_xy.py  -g LA
scripts/join_feature_data.py -g LA
scripts/unpickle_to_csv.py LA block
# scripts/unpickle_to_csv.py LA tract
scripts/unpickle_to_csv.py LA bg

echo "Processing data for MA ..."
scripts/extract_pop.py  -g MA > data/MA/MA_census_log.txt
scripts/extract_xy.py  -g MA
scripts/join_feature_data.py -g MA
scripts/unpickle_to_csv.py MA block
# scripts/unpickle_to_csv.py MA tract
scripts/unpickle_to_csv.py MA bg

echo "Processing data for MD ..."
scripts/extract_pop.py  -g MD > data/MD/MD_census_log.txt
scripts/extract_xy.py  -g MD
scripts/join_feature_data.py -g MD
scripts/unpickle_to_csv.py MD block
# scripts/unpickle_to_csv.py MD tract
scripts/unpickle_to_csv.py MD bg

# echo "Processing data for ME ..."
# scripts/extract_pop.py  -g ME > data/ME/ME_census_log.txt
# scripts/extract_xy.py  -g ME
# scripts/join_feature_data.py -g ME
# scripts/unpickle_to_csv.py ME block
# # scripts/unpickle_to_csv.py ME tract
# scripts/unpickle_to_csv.py ME bg

echo "Processing data for MI ..."
scripts/extract_pop.py  -g MI > data/MI/MI_census_log.txt
scripts/extract_xy.py  -g MI
scripts/join_feature_data.py -g MI
scripts/unpickle_to_csv.py MI block
# scripts/unpickle_to_csv.py MI tract
scripts/unpickle_to_csv.py MI bg

echo "Processing data for MN ..."
scripts/extract_pop.py  -g MN > data/MN/MN_census_log.txt
scripts/extract_xy.py  -g MN
scripts/join_feature_data.py -g MN
scripts/unpickle_to_csv.py MN block
# scripts/unpickle_to_csv.py MN tract
scripts/unpickle_to_csv.py MN bg

echo "Processing data for MO ..."
scripts/extract_pop.py  -g MO > data/MO/MO_census_log.txt
scripts/extract_xy.py  -g MO
scripts/join_feature_data.py -g MO
scripts/unpickle_to_csv.py MO block
# scripts/unpickle_to_csv.py MO tract
scripts/unpickle_to_csv.py MO bg

echo "Processing data for MS ..."
scripts/extract_pop.py  -g MS > data/MS/MS_census_log.txt
scripts/extract_xy.py  -g MS
scripts/join_feature_data.py -g MS
scripts/unpickle_to_csv.py MS block
# scripts/unpickle_to_csv.py MS tract
scripts/unpickle_to_csv.py MS bg

# echo "Processing data for MT ..."
# scripts/extract_pop.py  -g MT > data/MT/MT_census_log.txt
# scripts/extract_xy.py  -g MT
# scripts/join_feature_data.py -g MT
# scripts/unpickle_to_csv.py MT block
# # scripts/unpickle_to_csv.py MT tract
# scripts/unpickle_to_csv.py MT bg

echo "Processing data for NC ..."
scripts/extract_pop.py  -g NC > data/NC/NC_census_log.txt
scripts/extract_xy.py  -g NC
scripts/join_feature_data.py -g NC
scripts/unpickle_to_csv.py NC block
# scripts/unpickle_to_csv.py NC tract
scripts/unpickle_to_csv.py NC bg

# echo "Processing data for ND ..."
# scripts/extract_pop.py  -g ND > data/ND/ND_census_log.txt
# scripts/extract_xy.py  -g ND
# scripts/join_feature_data.py -g ND
# scripts/unpickle_to_csv.py ND block
# # scripts/unpickle_to_csv.py ND tract
# scripts/unpickle_to_csv.py ND bg

echo "Processing data for NE ..."
scripts/extract_pop.py  -g NE > data/NE/NE_census_log.txt
scripts/extract_xy.py  -g NE
scripts/join_feature_data.py -g NE
scripts/unpickle_to_csv.py NE block
# scripts/unpickle_to_csv.py NE tract
scripts/unpickle_to_csv.py NE bg

# echo "Processing data for NH ..."
# scripts/extract_pop.py  -g NH > data/NH/NH_census_log.txt
# scripts/extract_xy.py  -g NH
# scripts/join_feature_data.py -g NH
# scripts/unpickle_to_csv.py NH block
# # scripts/unpickle_to_csv.py NH tract
# scripts/unpickle_to_csv.py NH bg

echo "Processing data for NJ ..."
scripts/extract_pop.py  -g NJ > data/NJ/NJ_census_log.txt
scripts/extract_xy.py  -g NJ
scripts/join_feature_data.py -g NJ
scripts/unpickle_to_csv.py NJ block
# scripts/unpickle_to_csv.py NJ tract
scripts/unpickle_to_csv.py NJ bg

echo "Processing data for NM ..."
scripts/extract_pop.py  -g NM > data/NM/NM_census_log.txt
scripts/extract_xy.py  -g NM
scripts/join_feature_data.py -g NM
scripts/unpickle_to_csv.py NM block
# scripts/unpickle_to_csv.py NM tract
scripts/unpickle_to_csv.py NM bg

echo "Processing data for NV ..."
scripts/extract_pop.py  -g NV > data/NV/NV_census_log.txt
scripts/extract_xy.py  -g NV
scripts/join_feature_data.py -g NV
scripts/unpickle_to_csv.py NV block
# scripts/unpickle_to_csv.py NV tract
scripts/unpickle_to_csv.py NV bg

echo "Processing data for NY ..."
scripts/extract_pop.py  -g NY > data/NY/NY_census_log.txt
scripts/extract_xy.py  -g NY
scripts/join_feature_data.py -g NY
scripts/unpickle_to_csv.py NY block
# scripts/unpickle_to_csv.py NY tract
scripts/unpickle_to_csv.py NY bg

echo "Processing data for OH ..."
scripts/extract_pop.py  -g OH > data/OH/OH_census_log.txt
scripts/extract_xy.py  -g OH
scripts/join_feature_data.py -g OH
scripts/unpickle_to_csv.py OH block
# scripts/unpickle_to_csv.py OH tract
scripts/unpickle_to_csv.py OH bg

echo "Processing data for OK ..."
scripts/extract_pop.py  -g OK > data/OK/OK_census_log.txt
scripts/extract_xy.py  -g OK
scripts/join_feature_data.py -g OK
scripts/unpickle_to_csv.py OK block
# scripts/unpickle_to_csv.py OK tract
scripts/unpickle_to_csv.py OK bg

echo "Processing data for OR ..."
scripts/extract_pop.py  -g OR > data/OR/OR_census_log.txt
scripts/extract_xy.py  -g OR
scripts/join_feature_data.py -g OR
scripts/unpickle_to_csv.py OR block
# scripts/unpickle_to_csv.py OR tract
scripts/unpickle_to_csv.py OR bg

echo "Processing data for PA ..."
scripts/extract_pop.py  -g PA > data/PA/PA_census_log.txt
scripts/extract_xy.py  -g PA
scripts/join_feature_data.py -g PA
scripts/unpickle_to_csv.py PA block
# scripts/unpickle_to_csv.py PA tract
scripts/unpickle_to_csv.py PA bg

# echo "Processing data for RI ..."
# scripts/extract_pop.py  -g RI > data/RI/RI_census_log.txt
# scripts/extract_xy.py  -g RI
# scripts/join_feature_data.py -g RI
# scripts/unpickle_to_csv.py RI block
# # scripts/unpickle_to_csv.py RI tract
# scripts/unpickle_to_csv.py RI bg

echo "Processing data for SC ..."
scripts/extract_pop.py  -g SC > data/SC/SC_census_log.txt
scripts/extract_xy.py  -g SC
scripts/join_feature_data.py -g SC
scripts/unpickle_to_csv.py SC block
# scripts/unpickle_to_csv.py SC tract
scripts/unpickle_to_csv.py SC bg

# echo "Processing data for SD ..."
# scripts/extract_pop.py  -g SD > data/SD/SD_census_log.txt
# scripts/extract_xy.py  -g SD
# scripts/join_feature_data.py -g SD
# scripts/unpickle_to_csv.py SD block
# # scripts/unpickle_to_csv.py SD tract
# scripts/unpickle_to_csv.py SD bg

echo "Processing data for TN ..."
scripts/extract_pop.py  -g TN > data/TN/TN_census_log.txt
scripts/extract_xy.py  -g TN
scripts/join_feature_data.py -g TN
scripts/unpickle_to_csv.py TN block
# scripts/unpickle_to_csv.py TN tract
scripts/unpickle_to_csv.py TN bg

echo "Processing data for TX ..."
scripts/extract_pop.py  -g TX > data/TX/TX_census_log.txt
scripts/extract_xy.py  -g TX
scripts/join_feature_data.py -g TX
scripts/unpickle_to_csv.py TX block
# scripts/unpickle_to_csv.py TX tract
scripts/unpickle_to_csv.py TX bg

echo "Processing data for UT ..."
scripts/extract_pop.py  -g UT > data/UT/UT_census_log.txt
scripts/extract_xy.py  -g UT
scripts/join_feature_data.py -g UT
scripts/unpickle_to_csv.py UT block
# scripts/unpickle_to_csv.py UT tract
scripts/unpickle_to_csv.py UT bg

echo "Processing data for VA ..."
scripts/extract_pop.py  -g VA > data/VA/VA_census_log.txt
scripts/extract_xy.py  -g VA
scripts/join_feature_data.py -g VA
scripts/unpickle_to_csv.py VA block
# scripts/unpickle_to_csv.py VA tract
scripts/unpickle_to_csv.py VA bg

# echo "Processing data for VT ..."
# scripts/extract_pop.py  -g VT > data/VT/VT_census_log.txt
# scripts/extract_xy.py  -g VT
# scripts/join_feature_data.py -g VT
# scripts/unpickle_to_csv.py VT block
# # scripts/unpickle_to_csv.py VT tract
# scripts/unpickle_to_csv.py VT bg

echo "Processing data for WA ..."
scripts/extract_pop.py  -g WA > data/WA/WA_census_log.txt
scripts/extract_xy.py  -g WA
scripts/join_feature_data.py -g WA
scripts/unpickle_to_csv.py WA block
# scripts/unpickle_to_csv.py WA tract
scripts/unpickle_to_csv.py WA bg

echo "Processing data for WI ..."
scripts/extract_pop.py  -g WI > data/WI/WI_census_log.txt
scripts/extract_xy.py  -g WI
scripts/join_feature_data.py -g WI
scripts/unpickle_to_csv.py WI block
# scripts/unpickle_to_csv.py WI tract
scripts/unpickle_to_csv.py WI bg

# echo "Processing data for WV ..."
# scripts/extract_pop.py  -g WV > data/WV/WV_census_log.txt
# scripts/extract_xy.py  -g WV
# scripts/join_feature_data.py -g WV
# scripts/unpickle_to_csv.py WV block
# # scripts/unpickle_to_csv.py WV tract
# scripts/unpickle_to_csv.py WV bg

# echo "Processing data for WY ..."
# scripts/extract_pop.py  -g WY > data/WY/WY_census_log.txt
# scripts/extract_xy.py  -g WY
# scripts/join_feature_data.py -g WY
# scripts/unpickle_to_csv.py WY
# # scripts/unpickle_to_csv.py WY tract
# scripts/unpickle_to_csv.py WY bg

echo "... done preprocessing data."