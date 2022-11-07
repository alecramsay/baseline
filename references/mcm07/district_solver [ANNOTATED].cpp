#include "district_solver.h"
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <climits>

using namespace std;

// This is an annotated version of the original file district_solver.cpp.
// It contains my notes on how the moment-of-inertia solver works.

bool district_solver::solve_for_bigness()
{
  bool good;
  int i, j, smallest_diff, smallest_index, largest_diff, largest_index;

  // Bigness steps for districts are reset with each call to solve_for_bigness().
  fill(bigness_steps.begin(), bigness_steps.end(), 0x100000);
  compute_populations();
  while (true)
  {
    // make the most populous smaller (smallest refers to least people needed)
    good = true;
    smallest_diff = INT_MAX;
    for (i = 0; i < dist.size(); i++)
    {
      bigness_diff[i] = mean_population - district_pops[i];
      // cout << "bigness_diff[" << i << "]=" << bigness_diff[i] << endl;
      if (bigness_diff[i] < smallest_diff)
      {
        smallest_diff = bigness_diff[i];
        smallest_index = i;
      }
      if (bigness_diff[i] > size_tolerance || bigness_diff[i] < -size_tolerance)
        good = false;
    }
    // cout << "smallest index " << smallest_index << endl;
    // cout << "bigness " << dist[smallest_index].bigness << endl;
    if (good)
      return true;
    if (!bigness_steps[smallest_index])
      return false;
    dist[smallest_index].bigness -= bigness_steps[smallest_index];
    // cout << "new bigness " << dist[smallest_index].bigness << endl;
    compute_populations();
    while (district_pops[smallest_index] - mean_population < smallest_diff)
    {
      bigness_steps[smallest_index] >>= 1;
      dist[smallest_index].bigness += bigness_steps[smallest_index];
      // cout << "new bigness " << dist[smallest_index].bigness << endl;
      compute_populations();
    }
    if (district_pops[smallest_index] < mean_population)
      bigness_steps[smallest_index] >>= 1;
    // make the least populous bigger
    good = true;
    largest_diff = INT_MIN;
    for (i = 0; i < dist.size(); i++)
    {
      bigness_diff[i] = mean_population - district_pops[i];
      // cout << "bigness_diff[" << i << "]=" << bigness_diff[i] << endl;
      if (bigness_diff[i] > largest_diff)
      {
        largest_diff = bigness_diff[i];
        largest_index = i;
      }
      if (bigness_diff[i] > size_tolerance || bigness_diff[i] < -size_tolerance)
        good = false;
    }
    // cout << "largest index " << largest_index << endl;
    // cout << "bigness " << dist[largest_index].bigness << endl;
    if (good)
      return true;
    if (!bigness_steps[largest_index])
      return false;
    dist[largest_index].bigness += bigness_steps[largest_index];
    // cout << "new bigness " << dist[largest_index].bigness << endl;
    compute_populations();
    while (district_pops[largest_index] - mean_population > largest_diff)
    {
      bigness_steps[largest_index] >>= 1;
      dist[largest_index].bigness -= bigness_steps[largest_index];
      // cout << "new bigness " << dist[largest_index].bigness << endl;
      compute_populations();
    }
    if (district_pops[largest_index] > mean_population)
      bigness_steps[largest_index] >>= 1;
  }
}

void district_solver::find_minimum()
{
  int j, i, k;

  // I don't understand this hardcoded iteration.
  for (j = 0; j < 500; j++)
  {
    // cout << "Iteration " << j << endl;
    if (!solve_for_bigness())
    {
      cout << "Failure to converge at iteration " << j << endl;
      // return;
    }
    fill(district_sumx.begin(), district_sumx.end(), 0);
    fill(district_sumy.begin(), district_sumy.end(), 0);
    for (i = 0; i < pop.size(); i++)
    {
      k = closest_district(pop[i], dist);
      district_sumx[k] += (long long)pop[i].population * pop[i].longitude;
      district_sumy[k] += (long long)pop[i].population * pop[i].latitude;
    }
    for (i = 0; i < dist.size(); i++)
    {
      dist[i].longitude = district_sumx[i] / district_pops[i];
      dist[i].latitude = district_sumy[i] / district_pops[i];
      // cout << "District " << i << ' ' << dist[i].longitude << ',' <<
      // dist[i].latitude << endl;
    }
    // Population deviation tolerances are reduced linearly in small increments with each iteration.
    // After the first ~10 iterations, the rest will be using the smallest tolerance.
    if (size_tolerance > min_size_tolerance)
      size_tolerance -= min_size_tolerance;
  }
  for (i = 0; i < dist.size(); i++)
  {
    cout << "District " << i << " size " << district_pops[i] << endl;
  }
  // for(i=0;i<dist.size();i++) {
  //   cout << dist[i].longitude << "\t" << dist[i].latitude << "\t" <<
  //     dist[i].bigness << "\t" << dist[i].longitude*-.0003*cosine_avg << "\t" << dist[i].latitude*.0003;
  // }
}

void district_solver::read_data(istream &in)
{
  int nreps, npop, total_pop = 0, fullreps, i;
  int xmin = INT_MAX, xmax = 0, ymin = INT_MAX, ymax = 0;
  int area; // not used for anything yet
  long long coord;
  population_data p;
  in >> nreps;
  while (in >> npop)
  {
    // cout << npop << endl;
    if (npop > 0)
    {
      p.population = npop;
      total_pop += npop;
      in >> coord;
      p.latitude = coord / 300;
      if (p.latitude > ymax)
        ymax = p.latitude;
      if (p.latitude < ymin)
        ymin = p.latitude;
      in >> coord;
      p.longitude = coord / 300;
      if (p.longitude > xmax)
        xmax = p.longitude;
      if (p.longitude < xmin)
        xmin = p.longitude;
      pop.push_back(p);
    }
    else
    {
      in >> coord;
      in >> coord;
    }
    in >> area;
  }
  mean_population = total_pop / nreps;
  min_size_tolerance = mean_population / 50;
  size_tolerance = 10 * min_size_tolerance;
  cout << "District size is " << mean_population << endl;
  for (i = 0; i < pop.size(); i++)
  {
    fullreps = pop[i].population / mean_population;
    if (fullreps > 0)
    {
      nreps -= fullreps;
      pop[i].population -= fullreps * mean_population;
      cout << "County subdivision at " << pop[i].latitude << ',' << pop[i].longitude << " has enough people for " << fullreps << " full districts" << endl;
    }
  }
  dist.resize(nreps);
  srand(time(0));
  cosine_avg = cos(M_PI_2 * (ymin + ymax) / 600000.);
  cout << "cos(latitude)=" << cosine_avg << endl;
  xmin *= cosine_avg;
  xmax *= cosine_avg;
  for (i = 0; i < pop.size(); i++)
  {
    pop[i].longitude *= cosine_avg;
  }
  for (i = 0; i < nreps; i++)
  {
    // District bigness-es are initialized to zero before starting the process.
    // They're *not* reset after each iteration.
    dist[i].bigness = 0;

    // District centers are initialized to random points before starting the process.
    dist[i].latitude = ymin + rand() % (ymax - ymin + 1);
    dist[i].longitude = xmin + rand() % (xmax - xmin + 1);
  }
  district_pops.resize(nreps);
  district_sumx.resize(nreps);
  district_sumy.resize(nreps);
  bigness_diff.resize(nreps);
  bigness_steps.resize(nreps);
}

void district_solver::compute_populations()
{
  int i;
  fill(district_pops.begin(), district_pops.end(), 0);
  for (i = 0; i < pop.size(); i++)
    district_pops[closest_district(pop[i], dist)] += pop[i].population;
}

void district_solver::list_districts()
{
  int i, k;
  for (i = 0; i < pop.size(); i++)
  {
    k = closest_district(pop[i], dist);
    cout << k << '\t' << pop[i].longitude * -.0003 / cosine_avg << '\t'
         << pop[i].latitude * .0003 << endl;
  }
}
