# States

There are 37 states with three or more congressional districts.

TODO: We seemed to have stopped when were working on:
- Perf for NY, CA, and TX; and
- Water and land zero-population precincts, e.g., LA, MD, NJ, and UT

In extract_pop.py, I have the code to write out a CSV of unpopulated precincts,
but it's disabled. In extract_graph.py, I have the code to bridge over unpopulated
precincts, but it's implicitly disabled because I'm not logging them.

Current strategy: Leave all precincts in the data & adjacencies/graph and let Todd do the right thing.
Once everything is verified, clean up the code and ream out unused capabilities.

## Initial States

- NC <<< Run 6/21/23
- AZ* <<< TODO
- GA <<< TODO
- VA
- WA* <<< TODO

## Water-only Precincts

- IL* <<< TODO
- LA* <<< TODO
- MD* <<< TODO
- MI* <<< TODO
- NJ* <<< TODO

## Unpopulated Precincts

- KS* <<< TODO
- NV* <<< TODO
- UT* <<< TODO

## Runtime Issues

- NY* -- Has connectivity issues. <<< TODO
- CA* -- Uses tracts & BGs and has connectivity issues. <<< TODO

## Data Issues

- FL* -- The census shapes are bad. Use a custom script to ingest DRA's corrected shapes & data.

## Other States

- AL
- AR
- CO

- CT
- IA
- IN*
- KY*
- MA*
- MN*
- MO*
- MS
- NE

- NM
- OH*
- OK*
- OR* -- Uses BGs instead of VTDs.
- PA*
- SC
- TN*
- TX*
- WI*

An asterisk (*) indicates that the state has water-only precincts.