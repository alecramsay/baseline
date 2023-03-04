# Strategy for Fixing Stray Precincts

## Water-only Precincts

List water-only precincts, so they can be removed from the precinct-assignment file and adjacency graph. <<< DONE

## Precinct Assignment File

Create contiguous, population-balanced precinct assignment file:

* Create a precinct-assignment file w/o any splits -- take a real map & run the [Combine Split Precincts] tool, and export the precinct-assignment file <<< DONE
* Remove water-only precinct assignments <<< None in NC
* Equalize the district populations <<< TODO

## GEOID / Name Mapping

Create a GEOID / friendly name mapping, to facilitate graph modification <<< DONE

## Adjacency Graph

Create a fully connected adjacency graph w/o any water-only precincts:

* Generate an adjacency graph
* Revise the graph to remove water-only precincts <<< N/A in NC
* Make sure the *graph* is fully connected
* If not, find "islands" and connect them

* Generate the graph as pairs of neighbors
