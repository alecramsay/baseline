# Strategy for Fixing Stray Precincts

## Water-only Precincts

List water-only precincts, so they can be removed from the precinct-assignment file and adjacency graph.

## Precinct Assignment File

Create contiguous, population-balanced precinct assignment file:

* Create a precinct-assignment file w/o any splits
* Remove water-only precinct assignments
* Equalize the district populations

## GEOID / Name Mapping

Create a GEOID / friendly name mapping, to facilitate graph modification.

## Adjacency Graph

Create a fully connected adjacency graph w/o any water-only precincts:

* Generate an adjacency graph
* Revise the graph to remove water-only precincts
* Make sure the *graph* is fully connected
* If not, find "islands" and connect them