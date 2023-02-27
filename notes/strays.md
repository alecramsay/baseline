# Stray Precincts

The good news is that I *think* I can address most of these issues, by massaging the input to & output from your dccvt code. The one exception is the two instances of the state shapes & water issue.

## Embedded Shapes

There are three distinct scenarios of smaller precinct shapes being embedded w/in other larger ones:

* A single precinct is embedded w/in one other precinct (AR, CA, FL, GA, IA, IN, KS, LA, MI, MN, NV, NY, OH, OK, PA, VA, WA, WI)
* Multiple precincts -- sometimes connected, sometimes disjoint -- are embedded w/in another larger precinct (AR, MI, NE) -- Ditto.
* Zero-population, water-only precincts surround embedded, populated islands (including CA, NY)

These can be addressed by 1) aggregating the overlapping shapes before Balzer and disaggregating them after and 2) not including zero-population, water-only precincts in the input to Balzer. Note: The input might still contain unpopulated *land* precincts.

## Embedded Assignments

There's a different scenario in which one or more precincts are not fully embedded w/in a single larger precinct, but none of their neighbors are assigned to that same district:

* A single precinct  (AZ, CA, CO, GA, IA, IN, LA, MA!, MN, MO, NE, NJ, NV, NY, OH, OK, PA, TX, WA, WI) 
* A cluster of two precincts ... (CA, PA)
* A cluster of three precincts ... (CA)

It's most commonly a single precinct but occasionally can be a small cluster of 2-3. These assignments can be tweaked *after* Balzer (analogous to how we automatically reassign stray precincts in DRA). This would, of course, affect population deviation somewhat.

## Unassigned Assignments

I saw one weird case where a large unpopulated water-only precinct was not assigned to the nearest or adjacent neighbor:
 
* Illinois district 5

If, as noted above, I prune zero-population water-only precincts from the input to Balzer, this precinct won't get assigned. This is OK--we only need all *land* assigned to districts.

## State Shapes & Water

There are two instances in which maps are not contiguous due to the shape of the state not stray precincts:

* Louisiana -- https://davesredistricting.org/join/f3b2d7ed-cdeb-4a2c-99c6-f4db0b90f8e6
* Washington -- https://davesredistricting.org/join/91867c35-2c50-41d7-b15d-5e9534d50e13

I don't know how to address these. Let's discuss. They raise the issue of how you create Voronoi diagrams respecting state shape & contiguity.

## Miscellaneous

* Florida -- The geometry may be pretty messed up. Ignore it.
* Maryland -- Part of one multi polygonal water-only precinct is fully embedded w/in another. The map is reported as contiguous, but it *looks* discontiguous. This is OK.
* Parts of an un-split multi polygon precincts are sometimes fully embedded w/in another precinct (GA, IN, KS, MN) -- I don't understand how these *parts* are showing as discontiguous pieces. I need to sync w/ @Terry on this, as I think it's a bug.