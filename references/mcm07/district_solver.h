#ifndef _DISTRICT_SOLVER_H
#define _DISTRICT_SOLVER_H

#include "population_data.h"
#include "district_data.h"

#include <vector>
#include <iostream>

using namespace std;

inline long long distance_to(population_data &p, district_data &d)
{
  long long dx=p.latitude-d.latitude;
  long long dy=p.longitude-d.longitude;
  //cout << "displacement " << dx << ',' << dy << endl;
  return dx*dx+dy*dy-d.bigness;
}

inline int closest_district(population_data &p, vector<district_data> &v)
{
  int imin=0, i; 
  long long dmin=distance_to(p,v[0]), d;
  for(i=1;i<v.size();i++) {
    d=distance_to(p,v[i]);
    if(d<dmin) {
      imin=i;
      dmin=d;
    }
  }
  //cout << "closest_district size " << v.size() << " min " << imin << endl;
  return imin;
}

/* uncomment this if we decide to use GSL for finding the right bigness
inline int gsl_solverfunc(gsl_vector *bigness, void *params, gsl_vector *ans)
{
  ((district_solver *)params)->get_population_sizes(bigness,ans);
  return 0;
}
*/

class district_solver
{
  //friend int gsl_solverfunc(gsl_vector *bigness, void *params,
  //				gsl_vector *ans);
 public:
  void find_minimum();
  void read_data(istream &in);
  void list_districts();
 private:
  /* uncomment this if we decide to use gsl for finding the right bigness
  void get_population_sizes(gsl_vector *bigness, gsl_vector *ans) {
    int i;
    // zero out district_pops (check how to do in stl)
    dist[0].bigness=0;
    for(i=1;i<intbigness.size();i++)
      dist[i].bigness=(int)gsl_vector_get(bigness,i-1);
    for(i=0;i<pop.size();i++)
      district_pops[closest_district(pop[i],dist)]+=pop[i].population;
    for(i=1;i<pop.size();i++)
      gsl_vector_set(ans,i-1,district_pops[i]-district_pops[0]);
  }
  */

  bool solve_for_bigness();
  void compute_populations();
  vector<int> district_pops;
  vector<int> bigness_steps;
  vector<long long> district_sumx;
  vector<long long> district_sumy;
  vector<int> bigness_diff;
  vector<int> bigness_step;
  vector<population_data> pop;
  vector<district_data> dist;
  int mean_population;
  int size_tolerance;
  int min_size_tolerance;
  double cosine_avg;
};

#endif
