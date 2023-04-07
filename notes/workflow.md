# Processing Steps

Test initially on states that don't have any water-only precincts: XX, AZ, VA, and GA.
Then generalize for states with water-only precincts but no connectivity issues.
Finally, generalize to states with connectivity issues, like CA.

## Summary

- Download files
- Create output directories
- Find water-only precincts
- Preprocess data
- Generate a graph of precincts
- Create a baseline map
- Compare the candidate maps
- Choose a baseline

## Download files

- VTD names -- https://www.census.gov/geographies/reference-files/time-series/geo/name-lookup-tables.html
- Block assignments -- https://www.census.gov/geographies/reference-files/time-series/geo/block-assignment-files.html

## Create output directories

- data/XX
- intermediate/XX
- maps/XX

## Find water-only precincts

```
scripts/extract_water_only.py -s XX [> data/XX/XX_2020_water_only.csv]
```

Check the results in data/XX/XX_2020_water_only.csv.

## Preprocess data

```
scripts/extract_data.py -s XX
```

## Generate a graph of precincts

```
scripts/extract_graph.py -s XX
```

## Create a baseline map

```
scripts/baseline_state.py -s XX -i 100 -v > intermediate/XX/XX20C_log_100.txt
```

The above all together:

```
scripts/extract_water_only.py -s XX > data/XX/XX_2020_water_only.csv
scripts/extract_data.py -s XX
scripts/extract_graph.py -s XX
scripts/baseline_state.py -s XX -i 100 -v > intermediate/XX/XX20C_log_100.txt
```

## Compare the candidate maps

```
scripts/compare_maps.py -s XX -i 100 -v
```

- Copy any missing maps output to maps/XX/XX20C_missing.txt.
- Import XX20C_energies.csv into a spreadheet, and verify that the results are OK.

## Choose a baseline

- Copy the lowest energy baseline map to the maps/XX directory as XX20C_baseline_100.csv.

## Run the 'pg' workflow