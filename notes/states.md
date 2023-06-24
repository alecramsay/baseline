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

- NC <<< baselined
- AZ* <<< baselined
- GA <<< baselined
- VA <<< baselined
- WA* <<< baselined

## Water-only Precincts

- IL* <<< baselined
- LA* <<< baselined but TODO issue to resolve wrto population deviation
- MD* <<< baselined
- MI* <<< baselined
- NJ* <<< baselined

## Unpopulated Precincts

- KS* <<< baselined
- NV* <<< baselined
- UT* <<< baselined

## Runtime Issues

- NY* -- Has connectivity issues that had to be addressed by hand. <<< baselined: TODO - reported not contiguous
- CA* -- Uses tracts & BGs and has connectivity issues. <<< baselined

## Data Issues

- FL* -- The census shapes are bad. Use a custom script to ingest DRA's corrected shapes & data. <<< baselined

## Other States

- AL <<< baselined
- AR <<< baselined
- CO <<< baselined

- CT <<< baselined
- IA <<< baselined
- IN* <<< baselined
- KY* <<< baselined
- MA* <<< baselined
- MN* <<< baselined
- MO* <<< baselined
- MS <<< baselined
- NE <<< baselined

- NM <<< baselined
- OH* <<< baselined
- OK*
- OR* -- Uses BGs instead of VTDs. <<< baselined
- PA*
- SC
- TN*
- TX*
- WI*

An asterisk (*) indicates that the state has water-only precincts.