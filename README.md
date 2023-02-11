# Baseline Districts

Baseline legislatives districts derived only using a state's "population geography:" how many people live where in a state.

The purpose of this repository is to generate baseline districts for a state and type of map (congressional or upper or lower state house).
The process only uses census population data by feature location, where a feature is a census tract, block group, VTD, or block.
No other data is used, i.e., no demographic (race, ethnicity, age, etc.) data, no election data, no geometry/shapes, no county data, etc.

I introduced the concept of "baseline" districts in
[Baseline Congressional Districts: A Benchmark for Comparison](https://medium.com/redistricting-deep-dive/baseline-congressional-districts-a-benchmark-for-comparison-83b670608db3)
but I did not describe how to generate them.
Truth be told, while I had worked out a rough procedure that I used by hand at that time, I had not yet automated it.
I'm not sure it *could* be automated.

Todd Proebsting developed an automated solution based on Balzer's work.
The baseline districts in this repository were generated using his tool.

In contrast to other automated redistricting approaches, the purpose of baseline districts is *not* to suggest what
final district maps should be. They are intended as the *starting point* for drawing plans.
Because all maps at some level depend on the population geography of a state and baseline maps only depend on that,
they provide both a useful starting point for drawing plans (no blank slate) as well as a useful benchmark for 
comparing proposed and actual plans.

The basic idea is to produce "population compact" districts based on physics concept of moment of inertia.
Justin Levitt keyed me into the former. 
Some searching led me to Andrew Spann, Dan Gulotta, Daniel Kane's work on the latter.
Daniel Gulotta wrote a C++ implementation in the references/mcm07/ directory to
support their "Electoral Redistricting with Moment of Inertia and Diminishing Halves Models" winning paper at MCM 07.

The resulting districts are convex (and not oddly shaped like other simple geometric approaches).
