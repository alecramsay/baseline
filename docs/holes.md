# Analysis of Holes in NC Shapes

./cli.js describe -f file.geojson

State

$ ./cli.js describe -f ~/Downloads/baseline/data/NC/tl_2020_37_state20.geojson
0 polygons, 1 multipolygons, 1 total polygons, 0 total holes
32122 total points, 32122 when simplified.
Total Area: 139382764656.11783, Average Area: 139382764656

Tracts:

$ ./cli.js describe -f ~/Downloads/baseline/data/NC/tl_2020_37_tract.geojson
0 polygons, 2672 multipolygons, 2678 total polygons, 7 total holes
1967886 total points, 1967886 when simplified.
Total Area: 139389420937, Average Area: 52166699

Blockgroups

$ ./cli.js describe -f ~/Downloads/tl_2020_37_bg.geojson
0 polygons, 7111 multipolygons, 7116 total polygons, 11 total holes
3129956 total points, 3129956 when simplified.
Total Area: 139389420937, Average Area: 19601944

Blocks

$ ./cli.js describe -f ~/Downloads/baseline/data/NC/tl_2020_37_tabblock20.geojson
0 polygons, 236638 multipolygons, 236649 total polygons, 6966 total holes
18782232 total points, 18782232 when simplified.
Total Area: 139382764656.12137, Average Area: 589013

VTDs

$ ./cli.js describe -f ~/Downloads/baseline/data/NC/tl_2020_37_vtd20.geojson
0 polygons, 2666 multipolygons, 2671 total polygons, 6 total holes
1975422 total points, 1975422 when simplified.
Total Area: 139382764656.1252, Average Area: 52281607
