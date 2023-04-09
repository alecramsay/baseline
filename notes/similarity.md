# Similarity

If I want the baseline map to be the lowest energy map in the most commonly occurring energy valley
with n=100 randomized runs, then I need to be able to characterize how similar/different two sets of
assignments are.

- Maps == plans, and plans are d = # of districts sets of geographic units (e.g., precincts) assigned to those districts.
- The district id's (#'s) aren't stable though -- treating the plan as a point in d-space and computing a distance would finesse that.

Q. How to represent the geographic units assigned to each district though so that we can compute a distance?!?

A. Compute the population-weighted centroid of each district, and then use those as points in n-space to compute a distance.

## Resources

- https://scholar.google.com/scholar?q=signature+tree+set+similarity+search&hl=en&client=firefox-a&rls=org.mozilla:en-US:official&hs=sV2&um=1&ie=UTF-8&oi=scholart
- https://ieeexplore.ieee.org/abstract/document/1260783
- https://en.wikipedia.org/wiki/Equivalence_class
- https://en.wikipedia.org/wiki/Equivalence_relation