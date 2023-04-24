# History

This note captures some of the intellectual history of my work with Todd Proebsting to develop the concept of baseline districts:

- I started trying to port Andrew Spann, Dan Gulotta, Daniel Kane's C code to Python. I could never quite get the solver to reliably work with multiple states.
- When Todd got involved, he found and implemented Balzer's algorithm for computing Voronoi tessellations, adapting it slightly to redistricting.
- With that in hand, we proceeded through a series of experiments.
- First, we got Balzer to work with single pass, using various geographic granularities, e.g. blockgroups (BGs), blocks.
- Then, to try to make the resulting maps stable, invariant to specific starting points, we generated maps iterating (100x) on BGs, used those runs to find characteristic district centroids (sites), and then did a final finish run using blocks. The block granularity resulted in a huge number of split precincts -- basically every precinct along every district boundary!
- Then I realized I was forgetting a redistricting fundamental -- that precincts (VTDs) are basically the atomic unit of assignment, except when a few are split to achieve extreme population equality.
- With that realization in hand, I updated my scripts to iterate (100x) with precincts and then also use precincts in the finish run. This resolved the split precincts problem, but introduced another one: stray precincts from one district embedded within another adjacent one (near the shared boundary). IOW, the resulting districts for states were frequently not fully contiguous.
- Another related issue was that, in a few cases -- notably LA and WA -- the shapes of states were significantly concave and districts spanned the concavity.
- These issues caused us to try modifying the pure Balzer approach of randomly assigning the precincts to districts to assigning them based on a real, contiguous map and then running Balzer on the units (points) maintaining contiguity across all swaps. It seemed that this approach was very sensitive to the map chosen to establish the initial precinct-to-district assignments.
- TODO - Describe the current approach.

We are here.