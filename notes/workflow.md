# Processing Steps

Test initially on states that don't have any water-only precincts: NC, AZ, VA, and GA.
Then generalize for states with water-only precincts but no connectivity issues.
Finally, generalize to states with connectivity issues, like CA.

## Download files

- VTD names -- https://www.census.gov/geographies/reference-files/time-series/geo/name-lookup-tables.html
- Block assignments -- https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html

## Create data directory for the state


## Find water-only precincts

```
scripts/extract_water_only.py -s NC [> data/NC/NC_2020_water_only.csv]
```

## Preprocess data

```
scripts/extract_data.py -s NC
```

## Generate a graph of precincts

```
scripts/extract_graph.py -s NC
```

## Create a baseline map

```
scripts/baseline_state.py -s NC -i 100 -v > intermediate/NC/NC20C_log_100.txt
```

## All Together

```
scripts/extract_water_only.py -s XX > data/XX/XX_2020_water_only.csv
scripts/extract_data.py -s XX
scripts/extract_graph.py -s XX
scripts/baseline_state.py -s XX -i 100 -v > intermediate/XX/XX20C_log_100.txt
```