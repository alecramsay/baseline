#include "population_data.h"

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>

using namespace std;

void print_district(vector<population_data>::iterator begin,
		    vector<population_data>::iterator end)
{
  vector<population_data>::iterator it;
  cout << "Begin district" << endl;
  for(it=begin;it!=end;it++) {
    cout << it->longitude*300 << '\t' << it->latitude*300 << endl;
  }
}

struct pdsort_dir {
  pdsort_dir(double x, double y) : dx(x), dy(y) {}
  bool operator () (const population_data &p1, const population_data &p2) {
    return dx*p1.longitude+dy*p1.latitude<dx*p2.longitude+dy*p2.latitude;
  }
  double dx;
  double dy;
};

struct pds1 {
  pds1() {}
  long long operator () (long long s, const population_data &p) { return s+p.population; }
};

struct pdsx {
  pdsx() {}
  long long operator () (long long s, const population_data &p) { return s+(long long)p.population*p.longitude; }
};

struct pdsy {
  pdsy() {}
  long long operator () (long long s, const population_data &p) { return s+(long long)p.population*p.latitude; }
};

struct pdsx2 {
  pdsx2() {}
  long long operator () (long long s, const population_data &p) { return s+(long long)p.population*p.longitude*p.longitude; }
};

struct pdsxy {
  pdsxy() {}
  long long operator () (long long s, const population_data &p) { return s+(long long)p.population*p.longitude*p.latitude; }
};

struct pdsy2 {
  pdsy2() {}
  long long operator () (long long s, const population_data &p) { return s+(long long)p.population*p.latitude*p.latitude; }
};


void do_split(vector<population_data>::iterator begin,
	      vector<population_data>::iterator end,
	      vector<int>::iterator scratch_begin,
	      int n)
{
  if(n<=1) {
    print_district(begin,end);
    return;
  }
  //cout << &(*begin) << '\t' << &(*end) << '\t' << n << endl;
  long long s1=accumulate(begin,end,0LL,pds1());
  long long sx=accumulate(begin,end,0LL,pdsx());
  long long sy=accumulate(begin,end,0LL,pdsy());
  long long sx2=accumulate(begin,end,0LL,pdsx2());
  long long sxy=accumulate(begin,end,0LL,pdsxy());
  long long sy2=accumulate(begin,end,0LL,pdsy2());
  double c=((s1*sy2-sy*sy)-(s1*sx2-sx*sx))/2.;
  double s=s1*sxy-sx*sy;
  double r=sqrt(c*c+s*s);
  //cout << s1 << ' ' << sx << ' ' << sy << ' ' << sx2 << ' ' << sxy << ' ' << sy2 << endl;
  sort(begin,end,pdsort_dir(.78*s,r+c));
  int t=0;
  vector<population_data>::iterator it=begin;
  vector<int>::iterator sit=scratch_begin;
  for(;it!=end;it++,sit++) {
    t+=it->population;
    *sit=t;
  }
  //cout << t/n << endl;
  int halfn=n/2;
  int tnew=(t*halfn)/n;
  vector<int>::iterator scratch_end=scratch_begin+(end-begin);
  sit=lower_bound(scratch_begin,scratch_end,tnew);
  if(sit!=scratch_begin&&*sit+*(sit-1)>tnew) sit--;
  it=begin+(sit-scratch_begin+1);
  do_split(begin,it,scratch_begin,halfn);
  do_split(it,end,sit+1,n-halfn);
}

/*
void horizontal_split(vector<population_data>::iterator begin,
		      vector<population_data>::iterator end,
		      vector<int>::iterator scratch_begin,
		      int n);

void vertical_split(vector<population_data>::iterator begin,
		    vector<population_data>::iterator end,
		    vector<int>::iterator scratch_begin,
		    int n)
{
  if(n<=1) {
    print_district(begin,end);
    return;
  }
  //cout << &(*begin) << '\t' << &(*end) << '\t' << n << endl;
  sort(begin,end,pdsort_height());
  int t=0;
  vector<population_data>::iterator it=begin;
  vector<int>::iterator sit=scratch_begin;
  for(;it!=end;it++,sit++) {
    t+=it->population;
    *sit=t;
  }
  //cout << t/n << endl;
  int halfn=n/2;
  int tnew=(t*halfn)/n;
  vector<int>::iterator scratch_end=scratch_begin+(end-begin);
  sit=lower_bound(scratch_begin,scratch_end,tnew);
  if(sit!=scratch_begin&&*sit+*(sit-1)>tnew) sit--;
  it=begin+(sit-scratch_begin+1);
  horizontal_split(begin,it,scratch_begin,halfn);
  horizontal_split(it,end,sit+1,n-halfn);
}

void horizontal_split(vector<population_data>::iterator begin,
		      vector<population_data>::iterator end,
		      vector<int>::iterator scratch_begin,
		      int n)
{
  if(n<=1) {
    print_district(begin,end);
    return;
  }
  //cout << &(*begin) << '\t' << &(*end) << '\t' << n << endl;
  sort(begin,end,pdsort_width());
  int t=0;
  vector<population_data>::iterator it=begin;
  vector<int>::iterator sit=scratch_begin;
  for(;it!=end;it++,sit++) {
    t+=it->population;
    *sit=t;
  }
  int halfn=n/2;
  int tnew=(t*halfn)/n;
  //cout << halfn << endl;
  vector<int>::iterator scratch_end=scratch_begin+(end-begin);
  sit=lower_bound(scratch_begin,scratch_end,tnew);
  //cout << t << '\t' << *sit << endl;
  if(sit!=scratch_begin&&*sit+*(sit-1)>tnew) sit--;
  it=begin+(sit-scratch_begin+1);
  vertical_split(begin,it,scratch_begin,halfn);
  vertical_split(it,end,sit+1,n-halfn);
}
*/

int main(int argc, char **argv)
{
  if(argc>2) cerr << "usage dimh [file]" << endl;
  ifstream fin;
  if(argc==2) fin.open(argv[1]);
  istream &in=(argc==2)?fin:cin;
  vector<population_data> v;
  int ndist;
  int npop;
  long long coord;
  population_data p;
  in >> ndist;
  //cout << ndist << endl;
  while(in >> npop) {
    //cout << npop << endl;
    if(npop>0) {
      p.population=npop;
      in >> coord;
      p.latitude=coord/300;
      in >> coord;
      p.longitude=coord/300;
      v.push_back(p);
    }
    else {
      in >> coord;
      in >> coord;
    }
    in >> npop;
  }
  vector<int> scratch(v.size());
  do_split(v.begin(),v.end(),scratch.begin(),ndist);
  return 0;
}
