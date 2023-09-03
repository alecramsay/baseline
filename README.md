# Baseline Districts

Baseline legislatives districts are derived only using a state's "population geography:" how many people live where.

This repository generates baseline congressional districts for a state.
The process only uses census population by precinct location, where a precinct is either a census VTD or blockgroup.
No other data is used, i.e., no demographic (race, ethnicity, age, etc.) data, no election data, no geometry/shapes, no county data, etc.

In contrast to other automated redistricting approaches, the purpose of baseline districts is *not* to suggest what
final district maps should be. They are intended as the *starting point* for drawing plans.
Because all maps at some level depend on the population geography of a state and baseline maps only depend on that,
they provide both a useful starting point for drawing plans (no blank slate) as well as a useful benchmark for 
comparing proposed and actual plans.

Baseline districts are discussed in more detail in the the [Redistricting Alamanac: 2022](https://alecramsay.github.io/pg/).

## Dependencies

The code in this repository depends on two other repositories being installed locally and
being available on the `PYTHONPATH` environment variable:

- [pyutils](https://github.com/alecramsay/pyutils) - a set of Python utilities
- [dccvt](https://github.com/proebsting/dccvt) - Balzer's algorithm & associated redistricting utilities