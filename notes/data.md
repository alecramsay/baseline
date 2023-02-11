# Data

## Sources

* The 2020 census block populations come from https://github.com/dra2020/dra-data.
* The tract, blockgroup (BG), and block shapefiles come from https://www2.census.gov/geo/tiger/TIGER2020/.
* State shapefiles come from https://www2.census.gov/geo/tiger/TIGER2020PL/STATE/. <<< TODO - Is this needed?

Older:

* The block mapping files come from https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html.
* The VTD census data came from https://github.com/dra2020/vtd_data. The file names were rationalized to eliminate trailing '-1' and '-2' suffixes.

## Processing

For each state:

* Download the census block population JSON.
* Download tract, BG, and block shapefiles.
* Download the state shaefile. <<< TODO - Is this needed?

Run the preprocess_data.sh script.