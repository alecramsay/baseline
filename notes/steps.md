# Processing Steps

Find water-only precincts

Preprocess data, removing water-only precincts -- scripts/preprocess_state.py -s NC
- Extract & pickle VTD by block
- Extract & pickle pop by block
- Map blocks to VTDs -- scripts/extract_block_vtds.py -s NC
- Map VTD geoid to friendly names -- TODO: update extract_name_map.py to write results to a file

Generate a graph of precincts, removing water-only precincts

Export the official map to a BAF

Generate the initial.csv file <<< TODO
- Load the block-to-VTD (temp/NC_2020_block_vtd.pickle)
- Load the block population file for NC (temp/NC_2020_block_pop.pickle)
- Map VTD geoids to index offsets, using the points file (data/NC/NC_2020_vtd_data.csv)

- Read the BAF for the official NC map (data/NC/NC_2020_block_assignments.csv)
- Loop over the BAF, aggregating the block populations by VTD

- Write the results to initial.csv

Create a baseline map