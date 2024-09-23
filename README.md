# TSP Resolution
Resolution of TSP problem using exact and heuristic methods.

The Traveling Salesman Problem (TSP) is an optimization problem in which the goal is to find the most efficient route that passes through a set of predetermined locations.

In this project, we have coded different ways of solving this problem. Some of them are exacts and others are heuristic.

Considering the exact algorithms, we can find : 
- Held-Karp iterative algorithm
- 2 Linear Programs, using Miller-Tucker-Zemlin and Dantzig-Fulkerson-Johnson formulations (solved using Pulp package) 
  
And for the heuristic ones : 
- Nearest-Neighbor heuristic : we begin at one node, and for each city visited, we move to the nearest one, which has not been visited yet
- Lin-Kernighan heuristic (2-opt) : having a first hamiltonian circuit, we try iteratively to uncross crossed paths, in order to reduce the global cost
- Ant Colony heuristic : trying to reproduce ants behavior, in order to find a solution close to the best cycle.

Those algorithms can be tested on different instances (.tsp files). To change the algorithm or the instance, we just have to change the Strings *instance* (among *gr17.tsp*, *gr21.tsp*, *gr24.tsp* or others...) and *method* (among *ac*, *dfj*, *hk*, *lk*, *mtz* or *nn*).

## Contributors
Bastien DEMOLLIERE, Maryam EL FAKIR, Mathias LOMMEL, Aglaé PERRIN, Julie THOMAS 

---------------------------------------
Discrete Optimization

Department of __Applied Mathematics__

INSA Rennes, 2022-2023
