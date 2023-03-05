# Processing Steps

Test initially on states that don't have any water-only precincts: NC, AZ, VA, and GA.
Then generalize for states with water-only precincts but no connectivity issues.
Finally, generalize to states with connectivity issues, like CA.

## Download files

- VTD names -- https://www.census.gov/geographies/reference-files/time-series/geo/name-lookup-tables.html
- Block assignments -- https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html

## Find water-only precincts

```
scripts/extract_water_only.py -s NC [> data/NC/NC_2020_water_only.csv]
```

## Preprocess data

TODO - Remove water-only precincts

```
scripts/preprocess_state.py -s NC
```

## Generate a graph of precincts

TODO - Remove water-only precincts

```
scripts/extract_graph.py -s NC
```

## Export the official map as a BAF

From Dave's Redistricting

## Generate the initial.csv file 

```
scripts/make_initial_assignments.py -s NC
```

## Create a baseline map

```
scripts/baseline_state.py -s NC
```