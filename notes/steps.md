# Processing Steps

## Find water-only precincts

```
scripts/extract_water_only.py -s NC
```

## Preprocess data, removing water-only precincts

# TODO

```
scripts/preprocess_state.py -s NC
```

## Generate a graph of precincts, removing water-only precincts

TODO - Remove the 'vtd' argument (make it default)

```
scripts/extract_graph.py -s NC -u vtd
```

## Export the official map as a BAF

## Generate the initial.csv file 

```
scripts/make_initial_assignments.py -s NC
```

## Create a baseline map

TODO - Remove the 'congress' argument (make it default)

```
scripts/baseline_state.py NC congress
```