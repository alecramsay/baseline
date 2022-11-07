all: popsolver
popsolver_debug: main.cpp district_solver.cpp district_solver.h population_data.h district_data.h
	g++ -g3 main.cpp district_solver.cpp -o popsolver_debug
ny.ps: ny.gri log log2nydist
	./log2nydist; gri ny.gri
az.ps: az.gri azlog log2azdist
	./log2azdist; gri az.gri
il.ps: il.gri illog log2dist
	./log2dist il 19; gri il.gri
log : popsolver nydata2
	./popsolver nydata2 > log
azlog: popsolver azdata
	./popsolver azdata > azlog
illog: popsolver ildata
	./popsolver ildata > illog
popsolver: main.cpp district_solver.cpp district_solver.h population_data.h district_data.h
	g++ -O2 main.cpp district_solver.cpp -o popsolver
dh.ps: dh.gri dhlog makedh.pl
	./makedh.pl dhlog; gri dh.gri
dhlog: diminishing_halves nydata2
	./diminishing_halves nydata2 > dhlog
diminishing_halves: diminishing_halves.cpp
	g++ -O2 diminishing_halves.cpp -o diminishing_halves
