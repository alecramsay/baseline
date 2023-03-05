# Processing Steps

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

## Generate the initial.csv file 

```
scripts/make_initial_assignments.py -s NC
```

## Create a baseline map

```
scripts/baseline_state.py -s NC
```