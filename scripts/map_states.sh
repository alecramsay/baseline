#!/bin/bash
#
# Pre-process data for states
#
# For example:
#
# scripts/map_states.sh
#

echo "Mapping AL ..."
scripts/find_base_districts.py AL congress tract -v > results/AL/AL_2020_congress_tract_log.txt
# scripts/find_base_districts.py AL congress bg -v > results/AL/AL_2020_congress_bg_log.txt
# scripts/find_base_districts.py AL upper tract -v > results/AL/AL_2020_upper_tract_log.txt
# scripts/find_base_districts.py AL upper bg -v > results/AL/AL_2020_upper_bg_log.txt
# scripts/find_base_districts.py AL lower tract -v > results/AL/AL_2020_lower_tract_log.txt
# scripts/find_base_districts.py AL lower bg -v > results/AL/AL_2020_lower_bg_log.txt

# echo "Mapping AK ..."
# scripts/find_base_districts.py AK upper tract -v > results/AK/AK_2020_upper_tract_log.txt
# scripts/find_base_districts.py AK upper bg -v > results/AK/AK_2020_upper_bg_log.txt
# scripts/find_base_districts.py AK lower tract -v > results/AK/AK_2020_lower_tract_log.txt
# scripts/find_base_districts.py AK lower bg -v > results/AK/AK_2020_lower_bg_log.txt

echo "Mapping AZ ..."
scripts/find_base_districts.py AZ congress tract -v > results/AZ/AZ_2020_congress_tract_log.txt
# scripts/find_base_districts.py AZ congress bg -v > results/AZ/AZ_2020_congress_bg_log.txt
# scripts/find_base_districts.py AZ upper tract -v > results/AZ/AZ_2020_upper_tract_log.txt
# scripts/find_base_districts.py AZ upper bg -v > results/AZ/AZ_2020_upper_bg_log.txt

echo "Mapping AR ..."
scripts/find_base_districts.py AR congress tract -v > results/AR/AR_2020_congress_tract_log.txt
# scripts/find_base_districts.py AR congress bg -v > results/AR/AR_2020_congress_bg_log.txt
# scripts/find_base_districts.py AR upper tract -v > results/AR/AR_2020_upper_tract_log.txt
# scripts/find_base_districts.py AR upper bg -v > results/AR/AR_2020_upper_bg_log.txt
# scripts/find_base_districts.py AR lower tract -v > results/AR/AR_2020_lower_tract_log.txt
# scripts/find_base_districts.py AR lower bg -v > results/AR/AR_2020_lower_bg_log.txt

echo "Mapping CA ..."
scripts/find_base_districts.py CA congress tract -v > results/CA/CA_2020_congress_tract_log.txt
# scripts/find_base_districts.py CA congress bg -v > results/CA/CA_2020_congress_bg_log.txt
# scripts/find_base_districts.py CA upper tract -v > results/CA/CA_2020_upper_tract_log.txt
# scripts/find_base_districts.py CA upper bg -v > results/CA/CA_2020_upper_bg_log.txt
# scripts/find_base_districts.py CA lower tract -v > results/CA/CA_2020_lower_tract_log.txt
# scripts/find_base_districts.py CA lower bg -v > results/CA/CA_2020_lower_bg_log.txt

echo "Mapping CO ..."
scripts/find_base_districts.py CO congress tract -v > results/CO/CO_2020_congress_tract_log.txt
# scripts/find_base_districts.py CO congress bg -v > results/CO/CO_2020_congress_bg_log.txt
# scripts/find_base_districts.py CO upper tract -v > results/CO/CO_2020_upper_tract_log.txt
# scripts/find_base_districts.py CO upper bg -v > results/CO/CO_2020_upper_bg_log.txt
# scripts/find_base_districts.py CO lower tract -v > results/CO/CO_2020_lower_tract_log.txt
# scripts/find_base_districts.py CO lower bg -v > results/CO/CO_2020_lower_bg_log.txt

echo "Mapping CT ..."
scripts/find_base_districts.py CT congress tract -v > results/CT/CT_2020_congress_tract_log.txt
# scripts/find_base_districts.py CT congress bg -v > results/CT/CT_2020_congress_bg_log.txt
# scripts/find_base_districts.py CT upper tract -v > results/CT/CT_2020_upper_tract_log.txt
# scripts/find_base_districts.py CT upper bg -v > results/CT/CT_2020_upper_bg_log.txt
# scripts/find_base_districts.py CT lower tract -v > results/CT/CT_2020_lower_tract_log.txt
# scripts/find_base_districts.py CT lower bg -v > results/CT/CT_2020_lower_bg_log.txt

# echo "Mapping DE ..."
# scripts/find_base_districts.py DE upper tract -v > results/DE/DE_2020_upper_tract_log.txt
# scripts/find_base_districts.py DE upper bg -v > results/DE/DE_2020_upper_bg_log.txt
# scripts/find_base_districts.py DE lower tract -v > results/DE/DE_2020_lower_tract_log.txt
# scripts/find_base_districts.py DE lower bg -v > results/DE/DE_2020_lower_bg_log.txt

echo "Mapping FL ..."
scripts/find_base_districts.py FL congress tract -v > results/FL/FL_2020_congress_tract_log.txt
# scripts/find_base_districts.py FL congress bg -v > results/FL/FL_2020_congress_bg_log.txt
# scripts/find_base_districts.py FL upper tract -v > results/FL/FL_2020_upper_tract_log.txt
# scripts/find_base_districts.py FL upper bg -v > results/FL/FL_2020_upper_bg_log.txt
# scripts/find_base_districts.py FL lower tract -v > results/FL/FL_2020_lower_tract_log.txt
# scripts/find_base_districts.py FL lower bg -v > results/FL/FL_2020_lower_bg_log.txt

echo "Mapping GA ..."
scripts/find_base_districts.py GA congress tract -v > results/GA/GA_2020_congress_tract_log.txt
# scripts/find_base_districts.py GA congress bg -v > results/GA/GA_2020_congress_bg_log.txt
# scripts/find_base_districts.py GA upper tract -v > results/GA/GA_2020_upper_tract_log.txt
# scripts/find_base_districts.py GA upper bg -v > results/GA/GA_2020_upper_bg_log.txt
# scripts/find_base_districts.py GA lower tract -v > results/GA/GA_2020_lower_tract_log.txt
# scripts/find_base_districts.py GA lower bg -v > results/GA/GA_2020_lower_bg_log.txt

# echo "Mapping HI ..."
# scripts/find_base_districts.py HI congress tract -v > results/HI/HI_2020_congress_tract_log.txt
# scripts/find_base_districts.py HI congress bg -v > results/HI/HI_2020_congress_bg_log.txt
# scripts/find_base_districts.py HI upper tract -v > results/HI/HI_2020_upper_tract_log.txt
# scripts/find_base_districts.py HI upper bg -v > results/HI/HI_2020_upper_bg_log.txt
# scripts/find_base_districts.py HI lower tract -v > results/HI/HI_2020_lower_tract_log.txt
# scripts/find_base_districts.py HI lower bg -v > results/HI/HI_2020_lower_bg_log.txt

# echo "Mapping ID ..."
# scripts/find_base_districts.py ID congress tract -v > results/ID/ID_2020_congress_tract_log.txt
# scripts/find_base_districts.py ID congress bg -v > results/ID/ID_2020_congress_bg_log.txt
# scripts/find_base_districts.py ID upper tract -v > results/ID/ID_2020_upper_tract_log.txt
# scripts/find_base_districts.py ID upper bg -v > results/ID/ID_2020_upper_bg_log.txt

echo "Mapping IL ..."
scripts/find_base_districts.py IL congress tract -v > results/IL/IL_2020_congress_tract_log.txt
# scripts/find_base_districts.py IL congress bg -v > results/IL/IL_2020_congress_bg_log.txt
# scripts/find_base_districts.py IL upper tract -v > results/IL/IL_2020_upper_tract_log.txt
# scripts/find_base_districts.py IL upper bg -v > results/IL/IL_2020_upper_bg_log.txt
# scripts/find_base_districts.py IL lower tract -v > results/IL/IL_2020_lower_tract_log.txt
# scripts/find_base_districts.py IL lower bg -v > results/IL/IL_2020_lower_bg_log.txt

echo "Mapping IN ..."
scripts/find_base_districts.py IN congress tract -v > results/IN/IN_2020_congress_tract_log.txt
# scripts/find_base_districts.py IN congress bg -v > results/IN/IN_2020_congress_bg_log.txt
# scripts/find_base_districts.py IN upper tract -v > results/IN/IN_2020_upper_tract_log.txt
# scripts/find_base_districts.py IN upper bg -v > results/IN/IN_2020_upper_bg_log.txt
# scripts/find_base_districts.py IN lower tract -v > results/IN/IN_2020_lower_tract_log.txt
# scripts/find_base_districts.py IN lower bg -v > results/IN/IN_2020_lower_bg_log.txt

echo "Mapping IA ..."
scripts/find_base_districts.py IA congress tract -v > results/IA/IA_2020_congress_tract_log.txt
# scripts/find_base_districts.py IA congress bg -v > results/IA/IA_2020_congress_bg_log.txt
# scripts/find_base_districts.py IA upper tract -v > results/IA/IA_2020_upper_tract_log.txt
# scripts/find_base_districts.py IA upper bg -v > results/IA/IA_2020_upper_bg_log.txt
# scripts/find_base_districts.py IA lower tract -v > results/IA/IA_2020_lower_tract_log.txt
# scripts/find_base_districts.py IA lower bg -v > results/IA/IA_2020_lower_bg_log.txt

echo "Mapping KS ..."
scripts/find_base_districts.py KS congress tract -v > results/KS/KS_2020_congress_tract_log.txt
# scripts/find_base_districts.py KS congress bg -v > results/KS/KS_2020_congress_bg_log.txt
# scripts/find_base_districts.py KS upper tract -v > results/KS/KS_2020_upper_tract_log.txt
# scripts/find_base_districts.py KS upper bg -v > results/KS/KS_2020_upper_bg_log.txt
# scripts/find_base_districts.py KS lower tract -v > results/KS/KS_2020_lower_tract_log.txt
# scripts/find_base_districts.py KS lower bg -v > results/KS/KS_2020_lower_bg_log.txt

echo "Mapping KY ..."
scripts/find_base_districts.py KY congress tract -v > results/KY/KY_2020_congress_tract_log.txt
# scripts/find_base_districts.py KY congress bg -v > results/KY/KY_2020_congress_bg_log.txt
# scripts/find_base_districts.py KY upper tract -v > results/KY/KY_2020_upper_tract_log.txt
# scripts/find_base_districts.py KY upper bg -v > results/KY/KY_2020_upper_bg_log.txt
# scripts/find_base_districts.py KY lower tract -v > results/KY/KY_2020_lower_tract_log.txt
# scripts/find_base_districts.py KY lower bg -v > results/KY/KY_2020_lower_bg_log.txt

echo "Mapping LA ..."
scripts/find_base_districts.py LA congress tract -v > results/LA/LA_2020_congress_tract_log.txt
# scripts/find_base_districts.py LA congress bg -v > results/LA/LA_2020_congress_bg_log.txt
# scripts/find_base_districts.py LA upper tract -v > results/LA/LA_2020_upper_tract_log.txt
# scripts/find_base_districts.py LA upper bg -v > results/LA/LA_2020_upper_bg_log.txt
# scripts/find_base_districts.py LA lower tract -v > results/LA/LA_2020_lower_tract_log.txt
# scripts/find_base_districts.py LA lower bg -v > results/LA/LA_2020_lower_bg_log.txt

# echo "Mapping ME ..."
# scripts/find_base_districts.py ME congress tract -v > results/ME/ME_2020_congress_tract_log.txt
# scripts/find_base_districts.py ME congress bg -v > results/ME/ME_2020_congress_bg_log.txt
# scripts/find_base_districts.py ME upper tract -v > results/ME/ME_2020_upper_tract_log.txt
# scripts/find_base_districts.py ME upper bg -v > results/ME/ME_2020_upper_bg_log.txt
# scripts/find_base_districts.py ME lower tract -v > results/ME/ME_2020_lower_tract_log.txt
# scripts/find_base_districts.py ME lower bg -v > results/ME/ME_2020_lower_bg_log.txt

echo "Mapping MD ..."
scripts/find_base_districts.py MD congress tract -v > results/MD/MD_2020_congress_tract_log.txt
# scripts/find_base_districts.py MD congress bg -v > results/MD/MD_2020_congress_bg_log.txt
# scripts/find_base_districts.py MD upper tract -v > results/MD/MD_2020_upper_tract_log.txt
# scripts/find_base_districts.py MD upper bg -v > results/MD/MD_2020_upper_bg_log.txt
# scripts/find_base_districts.py MD lower tract -v > results/MD/MD_2020_lower_tract_log.txt
# scripts/find_base_districts.py MD lower bg -v > results/MD/MD_2020_lower_bg_log.txt

echo "Mapping MA ..."
scripts/find_base_districts.py MA congress tract -v > results/MA/MA_2020_congress_tract_log.txt
# scripts/find_base_districts.py MA congress bg -v > results/MA/MA_2020_congress_bg_log.txt
# scripts/find_base_districts.py MA upper tract -v > results/MA/MA_2020_upper_tract_log.txt
# scripts/find_base_districts.py MA upper bg -v > results/MA/MA_2020_upper_bg_log.txt
# scripts/find_base_districts.py MA lower tract -v > results/MA/MA_2020_lower_tract_log.txt
# scripts/find_base_districts.py MA lower bg -v > results/MA/MA_2020_lower_bg_log.txt

echo "Mapping MI ..."
scripts/find_base_districts.py MI congress tract -v > results/MI/MI_2020_congress_tract_log.txt
# scripts/find_base_districts.py MI congress bg -v > results/MI/MI_2020_congress_bg_log.txt
# scripts/find_base_districts.py MI upper tract -v > results/MI/MI_2020_upper_tract_log.txt
# scripts/find_base_districts.py MI upper bg -v > results/MI/MI_2020_upper_bg_log.txt
# scripts/find_base_districts.py MI lower tract -v > results/MI/MI_2020_lower_tract_log.txt
# scripts/find_base_districts.py MI lower bg -v > results/MI/MI_2020_lower_bg_log.txt

echo "Mapping MN ..."
scripts/find_base_districts.py MN congress tract -v > results/MN/MN_2020_congress_tract_log.txt
# scripts/find_base_districts.py MN congress bg -v > results/MN/MN_2020_congress_bg_log.txt
# scripts/find_base_districts.py MN upper tract -v > results/MN/MN_2020_upper_tract_log.txt
# scripts/find_base_districts.py MN upper bg -v > results/MN/MN_2020_upper_bg_log.txt
# scripts/find_base_districts.py MN lower tract -v > results/MN/MN_2020_lower_tract_log.txt
# scripts/find_base_districts.py MN lower bg -v > results/MN/MN_2020_lower_bg_log.txt

echo "Mapping MS ..."
scripts/find_base_districts.py MS congress tract -v > results/MS/MS_2020_congress_tract_log.txt
# scripts/find_base_districts.py MS congress bg -v > results/MS/MS_2020_congress_bg_log.txt
# scripts/find_base_districts.py MS upper tract -v > results/MS/MS_2020_upper_tract_log.txt
# scripts/find_base_districts.py MS upper bg -v > results/MS/MS_2020_upper_bg_log.txt
# scripts/find_base_districts.py MS lower tract -v > results/MS/MS_2020_lower_tract_log.txt
# scripts/find_base_districts.py MS lower bg -v > results/MS/MS_2020_lower_bg_log.txt

echo "Mapping MO ..."
scripts/find_base_districts.py MO congress tract -v > results/MO/MO_2020_congress_tract_log.txt
# scripts/find_base_districts.py MO congress bg -v > results/MO/MO_2020_congress_bg_log.txt
# scripts/find_base_districts.py MO upper tract -v > results/MO/MO_2020_upper_tract_log.txt
# scripts/find_base_districts.py MO upper bg -v > results/MO/MO_2020_upper_bg_log.txt
# scripts/find_base_districts.py MO lower tract -v > results/MO/MO_2020_lower_tract_log.txt
# scripts/find_base_districts.py MO lower bg -v > results/MO/MO_2020_lower_bg_log.txt

# echo "Mapping MT ..."
# scripts/find_base_districts.py MT congress tract -v > results/MT/MT_2020_congress_tract_log.txt
# scripts/find_base_districts.py MT congress bg -v > results/MT/MT_2020_congress_bg_log.txt
# scripts/find_base_districts.py MT upper tract -v > results/MT/MT_2020_upper_tract_log.txt
# scripts/find_base_districts.py MT upper bg -v > results/MT/MT_2020_upper_bg_log.txt
# scripts/find_base_districts.py MT lower tract -v > results/MT/MT_2020_lower_tract_log.txt
# scripts/find_base_districts.py MT lower bg -v > results/MT/MT_2020_lower_bg_log.txt

echo "Mapping NE ..."
scripts/find_base_districts.py NE congress tract -v > results/NE/NE_2020_congress_tract_log.txt
# scripts/find_base_districts.py NE congress bg -v > results/NE/NE_2020_congress_bg_log.txt
# scripts/find_base_districts.py NE upper tract -v > results/NE/NE_2020_upper_tract_log.txt
# scripts/find_base_districts.py NE upper bg -v > results/NE/NE_2020_upper_bg_log.txt

echo "Mapping NV ..."
scripts/find_base_districts.py NV congress tract -v > results/NV/NV_2020_congress_tract_log.txt
# scripts/find_base_districts.py NV congress bg -v > results/NV/NV_2020_congress_bg_log.txt
# scripts/find_base_districts.py NV upper tract -v > results/NV/NV_2020_upper_tract_log.txt
# scripts/find_base_districts.py NV upper bg -v > results/NV/NV_2020_upper_bg_log.txt
# scripts/find_base_districts.py NV lower tract -v > results/NV/NV_2020_lower_tract_log.txt
# scripts/find_base_districts.py NV lower bg -v > results/NV/NV_2020_lower_bg_log.txt

# echo "Mapping NH ..."
# scripts/find_base_districts.py NH congress tract -v > results/NH/NH_2020_congress_tract_log.txt
# scripts/find_base_districts.py NH congress bg -v > results/NH/NH_2020_congress_bg_log.txt
# scripts/find_base_districts.py NH upper tract -v > results/NH/NH_2020_upper_tract_log.txt
# scripts/find_base_districts.py NH upper bg -v > results/NH/NH_2020_upper_bg_log.txt
# scripts/find_base_districts.py NH lower tract -v > results/NH/NH_2020_lower_tract_log.txt
# scripts/find_base_districts.py NH lower bg -v > results/NH/NH_2020_lower_bg_log.txt

echo "Mapping NJ ..."
scripts/find_base_districts.py NJ congress tract -v > results/NJ/NJ_2020_congress_tract_log.txt
# scripts/find_base_districts.py NJ congress bg -v > results/NJ/NJ_2020_congress_bg_log.txt
# scripts/find_base_districts.py NJ upper tract -v > results/NJ/NJ_2020_upper_tract_log.txt
# scripts/find_base_districts.py NJ upper bg -v > results/NJ/NJ_2020_upper_bg_log.txt

echo "Mapping NM ..."
scripts/find_base_districts.py NM congress tract -v > results/NM/NM_2020_congress_tract_log.txt
# scripts/find_base_districts.py NM congress bg -v > results/NM/NM_2020_congress_bg_log.txt
# scripts/find_base_districts.py NM upper tract -v > results/NM/NM_2020_upper_tract_log.txt
# scripts/find_base_districts.py NM upper bg -v > results/NM/NM_2020_upper_bg_log.txt
# scripts/find_base_districts.py NM lower tract -v > results/NM/NM_2020_lower_tract_log.txt
# scripts/find_base_districts.py NM lower bg -v > results/NM/NM_2020_lower_bg_log.txt

echo "Mapping NY ..."
scripts/find_base_districts.py NY congress tract -v > results/NY/NY_2020_congress_tract_log.txt
# scripts/find_base_districts.py NY congress bg -v > results/NY/NY_2020_congress_bg_log.txt
# scripts/find_base_districts.py NY upper tract -v > results/NY/NY_2020_upper_tract_log.txt
# scripts/find_base_districts.py NY upper bg -v > results/NY/NY_2020_upper_bg_log.txt
# scripts/find_base_districts.py NY lower tract -v > results/NY/NY_2020_lower_tract_log.txt
# scripts/find_base_districts.py NY lower bg -v > results/NY/NY_2020_lower_bg_log.txt

echo "Mapping NC ..."
scripts/find_base_districts.py NC congress tract -v > results/NC/NC_2020_congress_tract_log.txt
# scripts/find_base_districts.py NC congress bg -v > results/NC/NC_2020_congress_bg_log.txt
# scripts/find_base_districts.py NC upper tract -v > results/NC/NC_2020_upper_tract_log.txt
# scripts/find_base_districts.py NC upper bg -v > results/NC/NC_2020_upper_bg_log.txt
# scripts/find_base_districts.py NC lower tract -v > results/NC/NC_2020_lower_tract_log.txt
# scripts/find_base_districts.py NC lower bg -v > results/NC/NC_2020_lower_bg_log.txt

# echo "Mapping ND ..."
# scripts/find_base_districts.py ND upper tract -v > results/ND/ND_2020_upper_tract_log.txt
# scripts/find_base_districts.py ND upper bg -v > results/ND/ND_2020_upper_bg_log.txt
# scripts/find_base_districts.py ND lower tract -v > results/ND/ND_2020_lower_tract_log.txt
# scripts/find_base_districts.py ND lower bg -v > results/ND/ND_2020_lower_bg_log.txt

echo "Mapping OH ..."
scripts/find_base_districts.py OH congress tract -v > results/OH/OH_2020_congress_tract_log.txt
# scripts/find_base_districts.py OH congress bg -v > results/OH/OH_2020_congress_bg_log.txt
# scripts/find_base_districts.py OH upper tract -v > results/OH/OH_2020_upper_tract_log.txt
# scripts/find_base_districts.py OH upper bg -v > results/OH/OH_2020_upper_bg_log.txt
# scripts/find_base_districts.py OH lower tract -v > results/OH/OH_2020_lower_tract_log.txt
# scripts/find_base_districts.py OH lower bg -v > results/OH/OH_2020_lower_bg_log.txt

echo "Mapping OK ..."
scripts/find_base_districts.py OK congress tract -v > results/OK/OK_2020_congress_tract_log.txt
# scripts/find_base_districts.py OK congress bg -v > results/OK/OK_2020_congress_bg_log.txt
# scripts/find_base_districts.py OK upper tract -v > results/OK/OK_2020_upper_tract_log.txt
# scripts/find_base_districts.py OK upper bg -v > results/OK/OK_2020_upper_bg_log.txt
# scripts/find_base_districts.py OK lower tract -v > results/OK/OK_2020_lower_tract_log.txt
# scripts/find_base_districts.py OK lower bg -v > results/OK/OK_2020_lower_bg_log.txt

echo "Mapping OR ..."
scripts/find_base_districts.py OR congress tract -v > results/OR/OR_2020_congress_tract_log.txt
# scripts/find_base_districts.py OR congress bg -v > results/OR/OR_2020_congress_bg_log.txt
# scripts/find_base_districts.py OR upper tract -v > results/OR/OR_2020_upper_tract_log.txt
# scripts/find_base_districts.py OR upper bg -v > results/OR/OR_2020_upper_bg_log.txt
# scripts/find_base_districts.py OR lower tract -v > results/OR/OR_2020_lower_tract_log.txt
# scripts/find_base_districts.py OR lower bg -v > results/OR/OR_2020_lower_bg_log.txt

echo "Mapping PA ..."
scripts/find_base_districts.py PA congress tract -v > results/PA/PA_2020_congress_tract_log.txt
# scripts/find_base_districts.py PA congress bg -v > results/PA/PA_2020_congress_bg_log.txt
# scripts/find_base_districts.py PA upper tract -v > results/PA/PA_2020_upper_tract_log.txt
# scripts/find_base_districts.py PA upper bg -v > results/PA/PA_2020_upper_bg_log.txt
# scripts/find_base_districts.py PA lower tract -v > results/PA/PA_2020_lower_tract_log.txt
# scripts/find_base_districts.py PA lower bg -v > results/PA/PA_2020_lower_bg_log.txt

# echo "Mapping RI ..."
# scripts/find_base_districts.py RI congress tract -v > results/RI/RI_2020_congress_tract_log.txt
# scripts/find_base_districts.py RI congress bg -v > results/RI/RI_2020_congress_bg_log.txt
# scripts/find_base_districts.py RI upper tract -v > results/RI/RI_2020_upper_tract_log.txt
# scripts/find_base_districts.py RI upper bg -v > results/RI/RI_2020_upper_bg_log.txt
# scripts/find_base_districts.py RI lower tract -v > results/RI/RI_2020_lower_tract_log.txt
# scripts/find_base_districts.py RI lower bg -v > results/RI/RI_2020_lower_bg_log.txt

echo "Mapping SC ..."
scripts/find_base_districts.py SC congress tract -v > results/SC/SC_2020_congress_tract_log.txt
# scripts/find_base_districts.py SC congress bg -v > results/SC/SC_2020_congress_bg_log.txt
# scripts/find_base_districts.py SC upper tract -v > results/SC/SC_2020_upper_tract_log.txt
# scripts/find_base_districts.py SC upper bg -v > results/SC/SC_2020_upper_bg_log.txt
# scripts/find_base_districts.py SC lower tract -v > results/SC/SC_2020_lower_tract_log.txt
# scripts/find_base_districts.py SC lower bg -v > results/SC/SC_2020_lower_bg_log.txt

# echo "Mapping SD ..."
# scripts/find_base_districts.py SD upper tract -v > results/SD/SD_2020_upper_tract_log.txt
# scripts/find_base_districts.py SD upper bg -v > results/SD/SD_2020_upper_bg_log.txt
# scripts/find_base_districts.py SD lower tract -v > results/SD/SD_2020_lower_tract_log.txt
# scripts/find_base_districts.py SD lower bg -v > results/SD/SD_2020_lower_bg_log.txt

echo "Mapping TN ..."
scripts/find_base_districts.py TN congress tract -v > results/TN/TN_2020_congress_tract_log.txt
# scripts/find_base_districts.py TN congress bg -v > results/TN/TN_2020_congress_bg_log.txt
# scripts/find_base_districts.py TN upper tract -v > results/TN/TN_2020_upper_tract_log.txt
# scripts/find_base_districts.py TN upper bg -v > results/TN/TN_2020_upper_bg_log.txt
# scripts/find_base_districts.py TN lower tract -v > results/TN/TN_2020_lower_tract_log.txt
# scripts/find_base_districts.py TN lower bg -v > results/TN/TN_2020_lower_bg_log.txt

echo "Mapping TX ..."
scripts/find_base_districts.py TX congress tract -v > results/TX/TX_2020_congress_tract_log.txt
# scripts/find_base_districts.py TX congress bg -v > results/TX/TX_2020_congress_bg_log.txt
# scripts/find_base_districts.py TX upper tract -v > results/TX/TX_2020_upper_tract_log.txt
# scripts/find_base_districts.py TX upper bg -v > results/TX/TX_2020_upper_bg_log.txt
# scripts/find_base_districts.py TX lower tract -v > results/TX/TX_2020_lower_tract_log.txt
# scripts/find_base_districts.py TX lower bg -v > results/TX/TX_2020_lower_bg_log.txt

echo "Mapping UT ..."
scripts/find_base_districts.py UT congress tract -v > results/UT/UT_2020_congress_tract_log.txt
# scripts/find_base_districts.py UT congress bg -v > results/UT/UT_2020_congress_bg_log.txt
# scripts/find_base_districts.py UT upper tract -v > results/UT/UT_2020_upper_tract_log.txt
# scripts/find_base_districts.py UT upper bg -v > results/UT/UT_2020_upper_bg_log.txt
# scripts/find_base_districts.py UT lower tract -v > results/UT/UT_2020_lower_tract_log.txt
# scripts/find_base_districts.py UT lower bg -v > results/UT/UT_2020_lower_bg_log.txt

# echo "Mapping VT ..."
# scripts/find_base_districts.py VT upper tract -v > results/VT/VT_2020_upper_tract_log.txt
# scripts/find_base_districts.py VT upper bg -v > results/VT/VT_2020_upper_bg_log.txt
# scripts/find_base_districts.py VT lower tract -v > results/VT/VT_2020_lower_tract_log.txt
# scripts/find_base_districts.py VT lower bg -v > results/VT/VT_2020_lower_bg_log.txt

echo "Mapping VA ..."
scripts/find_base_districts.py VA congress tract -v > results/VA/VA_2020_congress_tract_log.txt
# scripts/find_base_districts.py VA congress bg -v > results/VA/VA_2020_congress_bg_log.txt
# scripts/find_base_districts.py VA upper tract -v > results/VA/VA_2020_upper_tract_log.txt
# scripts/find_base_districts.py VA upper bg -v > results/VA/VA_2020_upper_bg_log.txt
# scripts/find_base_districts.py VA lower tract -v > results/VA/VA_2020_lower_tract_log.txt
# scripts/find_base_districts.py VA lower bg -v > results/VA/VA_2020_lower_bg_log.txt

echo "Mapping WA ..."
scripts/find_base_districts.py WA congress tract -v > results/WA/WA_2020_congress_tract_log.txt
# scripts/find_base_districts.py WA congress bg -v > results/WA/WA_2020_congress_bg_log.txt
# scripts/find_base_districts.py WA upper tract -v > results/WA/WA_2020_upper_tract_log.txt
# scripts/find_base_districts.py WA upper bg -v > results/WA/WA_2020_upper_bg_log.txt

# echo "Mapping WV ..."
# scripts/find_base_districts.py WV congress tract -v > results/WV/WV_2020_congress_tract_log.txt
# scripts/find_base_districts.py WV congress bg -v > results/WV/WV_2020_congress_bg_log.txt
# scripts/find_base_districts.py WV upper tract -v > results/WV/WV_2020_upper_tract_log.txt
# scripts/find_base_districts.py WV upper bg -v > results/WV/WV_2020_upper_bg_log.txt
# scripts/find_base_districts.py WV lower tract -v > results/WV/WV_2020_lower_tract_log.txt
# scripts/find_base_districts.py WV lower bg -v > results/WV/WV_2020_lower_bg_log.txt

echo "Mapping WI ..."
scripts/find_base_districts.py WI congress tract -v > results/WI/WI_2020_congress_tract_log.txt
# scripts/find_base_districts.py WI congress bg -v > results/WI/WI_2020_congress_bg_log.txt
# scripts/find_base_districts.py WI upper tract -v > results/WI/WI_2020_upper_tract_log.txt
# scripts/find_base_districts.py WI upper bg -v > results/WI/WI_2020_upper_bg_log.txt
# scripts/find_base_districts.py WI lower tract -v > results/WI/WI_2020_lower_tract_log.txt
# scripts/find_base_districts.py WI lower bg -v > results/WI/WI_2020_lower_bg_log.txt

# echo "Mapping WY ..."
# scripts/find_base_districts.py WY upper tract -v > results/WY/WY_2020_upper_tract_log.txt
# scripts/find_base_districts.py WY upper bg -v > results/WY/WY_2020_upper_bg_log.txt
# scripts/find_base_districts.py WY lower tract -v > results/WY/WY_2020_lower_tract_log.txt
# scripts/find_base_districts.py WY lower bg -v > results/WY/WY_2020_lower_bg_log.txt
