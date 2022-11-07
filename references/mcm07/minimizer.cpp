#include "minimizer.h"
#include <vector>

using std::vector;

double minimizer_func(const gsl_vector *v, void *params)
{
  int size=v->size/2;
  vector<int> x(v->size);
  vector<int> y(v->size);
  population_data &d = *(population_data *)params;
  int i;
  for(i=0;i<x->size;) {
    centers[i]=(int) gsl_vector_get(x,i);
    if(centers[i]<0) centers[i]=0;
    if(centers[i]>=d.width()) centers[i]=d.width()-1;
    i++;
    centers[i]=(int) gsl_vector_get(x,i);
    if(centers[i]<0) centers[i]=0;
    if(centers[i]>=d.height()) centers[i]=d.height()-1;
    i++;
  }
}
