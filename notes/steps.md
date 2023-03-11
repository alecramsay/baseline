# Processing Steps

Test initially on states that don't have any water-only precincts: NC, AZ, VA, and GA.
Then generalize for states with water-only precincts but no connectivity issues.
Finally, generalize to states with connectivity issues, like CA.

## Ready

- NC: nearly exact (+/- 1 person per district)
- GA: very small officially and made smaller by the initial assignments script

## Download files

- VTD names -- https://www.census.gov/geographies/reference-files/time-series/geo/name-lookup-tables.html
- Block assignments -- https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html

## Find water-only precincts

```
scripts/extract_water_only.py -s NC [> data/NC/NC_2020_water_only.csv]
```

## Preprocess data

```
scripts/preprocess_state.py -s NC
```

## Generate a graph of precincts

```
scripts/extract_graph.py -s NC
```

## Export the official map as a BAF

From Dave's Redistricting

## Generate the initial.csv file 

```
scripts/make_initial_assignments.py -s NC
```

Use the -e flag to spread out the excess population to underpopulated districts.

## Create a baseline map

```
scripts/baseline_state.py -s NC
```

## All Together

```
scripts/extract_water_only.py -s XX > data/XX/XX_2020_water_only.csv
scripts/preprocess_state.py -s XX
scripts/extract_graph.py -s XX
scripts/make_initial_assignments.py -s XX -e -v
scripts/baseline_state.py -s XX
```