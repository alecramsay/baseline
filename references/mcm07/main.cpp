#include "district_solver.h"

#include <iostream>
#include <fstream>

using namespace std;

// Right now I want the distance squared to fit in an unsigned int
// for performance reasons.  If our program is running quickly and
// we care about extreme accuracy, we can use long longs instead.

int main(int argc, char **argv)
{
  if(argc>2) {
    cerr << "usage: popsolver [datafile]" << endl;
    return 1;
  }
  district_solver d;
  if(argc==2) {
    ifstream in(argv[1]);
    d.read_data(in);
  }
  else d.read_data(cin);
  d.find_minimum();
  d.list_districts();
  return 0;
}
