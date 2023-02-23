# Data

## Sources

* The 2020 census block populations come from https://github.com/dra2020/dra-data.
* The VTD shapesfiles come from https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/VTD/2020/.
* The tract, blockgroup (BG), and block shapefiles come from https://www2.census.gov/geo/tiger/TIGER2020/.

Due to their size, these data are stored locally (i.e., not in the repo).

Older:

* The block mapping files come from https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html.
* The VTD census data came from https://github.com/dra2020/vtd_data. The file names were rationalized to eliminate trailing '-1' and '-2' suffixes.
* State shapefiles come from https://www2.census.gov/geo/tiger/TIGER2020PL/STATE/.

## Processing

For each state:

* Download the census block population JSON.
* Download BG and block shapefiles.

Run the preprocess_data.sh script.

Then generate baseline districts for each state TODO.

## Generating Seeds (LEGACY)

If you want to generate plastic seeds to use instead of random ones, 
download the state shapefile, and then run the generate_seeds.py script.


TODO - Update these notes.