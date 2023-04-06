# North Carolina Congressional Baseline

I believe we have a defensible [baseline map](https://davesredistricting.org/join/a7ac927b-2dfc-4e79-b954-b9c43b7fe12f) for North Carolina!

That map was one of 1,000 iterations. The [baseline map](https://davesredistricting.org/join/48ea8e69-e6b8-4ddf-89f1-bcc65254ff00) using 100 iterations is very very similar.

## What I Did

- I ran clean.sh 1,000 times, starting with a repeatable seed and incrementing it on each run (so I can repeat the run).
- NOTE -- At some point, I'll want to flesh out a simple summary of the process (steps) that clean.sh executes.
- I logged the output to a file.
- Then I culled the energies for each map from that log and calculated four metrics for each. I describe the metrics below.
- The results are in the attached spreadsheet, sorted by energy. The data for each baseline candidate is on the DATA tab, and the results are summarized one the SUMMARY tab.

## Metrics

I didn't need any more data to compute the metrics. I realized that the end metrics that we imagined calculating for each map -- things like proportionality, competitiveness, opportunity for minority representation, compactness, and county splitting -- can only differ if the precinct assignments differ (duh). IOW, if the assignments are the same, the end analytics will be the same. Only if they're significantly different would actually computing the end metrics be important.

So, I have characterized how similar/different the assignments are between each map and the lowest energy map (weighted by population, of course) as a first-order approximation. In some sense, these metrics represent an "edit distance."

For each map, I computed four values:

- DELTA -- How much the map's energy deviated from the lowest energy of all runs. This is a percentage shown as a fraction [0–1].
- SHARED -- How much the current map's districts share with the lowest energy map's districts. I average this over all districts. Again, a percentage shown as a fraction [0–1].
- UOM -- The uncertainty of membership metric (see below).
- ES -- The effective splits metric (see below).

In the NOTES column, I note which maps are lowest energy in the 1-10, 1-100, and 1-1000 ranges.

The last two metrics come from [Turning Communities Of Interest Into A Rigorous Standard For Fair Districting](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3828800). They're a solid proposal for how to characterize how much a set of districts split communities of interest, and we compute them in DRA, both when analyzing community splitting but also when comparing the diff between two full maps like we're doing here.

## Results

On the SUMMARY tab, I've done some simple analysis:

- The table at the top shows statistics for all the runs.
- Of the 1,000 runs, only 7 failed (0.70%).
- Of the remaining 993 runs, 953 (96%) had energy < 1% greater than the lowest energy overall -- i.e., almost all maps had similar energies. 
- What these two things mean together is, I think, that the process occasionally (3-4% of the time) gets stuck in some suboptimal configuration, but most of the time it essentially finds the same lowest energy partitioning.

The second table characterizes the 953 maps in that space:

- The median delta energy was just 0.5%.
- Of these maps, 809 (85%) shared > 95% of the population-weighted assignments -- i.e., most of these maps were very very similar  in terms of the shapes of the districts. 
- The median percentage of population-weighted shared assignments was 96.54%.
- The raw values for UoM and ES are hard to intuit -- which is why I included the simple-to-understand percentage of shared assignments! -- but I normalized them offline and they're low/good. These more formal, more technical metrics will be useful in a more academic/publishing context.

The bottom line is that I think it's safe to conclude that almost all these runs produce roughly the same assignments, so the lowest energy map is a very defensible baseline. Moreover, the lowest energy map for 100 runs is quite similar to the lowest energy maps for 1,000 runs, so 100 iterations seems like enough. 

Someone could, of course, find a map that is even lower energy, but, having done 1,000 iterations, it seems very unlikely that the broad strokes of the districts will be substantially different. And if they are, that's good too.