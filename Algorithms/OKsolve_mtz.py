import numpy as np
import pulp

def solve_mtz(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M by solving its
    Miller–Tucker–Zemlin formulation.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.

    Returns
    -------
    cost : int or float
        The solution tour cost.
        
    """
    n=len(M[0,:])
    
    #Définition du problème
    tsp=pulp.LpProblem("TSP",sense=pulp.LpMinimize)
    
    #Variable de décision lowBound=0, upBound=n, 
    X = pulp.LpVariable.dicts("X",((i,j) for i in range(0,n) for j in range(0,n)), lowBound=0, upBound=1,cat='Binary')
    u = pulp.LpVariable.dicts("u",(i for i in range(0,n)), lowBound=1, cat='Continuous')
    #Fonction à minimiser
    tsp += pulp.lpSum([X[i,j]*M[i,j] for i in range(0,n) for j in range(0,n)])
    
    #Contraintes
    tsp += u[0]==1                                          #Contrainte sur u_0
    
    for i in range(0,n):
        tsp += X[i,i]==0
        tsp += pulp.lpSum([X[i,j] for j in range(0,n)])==1  #Contrainte sur les lignes de X
        tsp += pulp.lpSum([X[j,i] for j in range(0,n)])==1  #Contrainte sur les colonnes de X
        
        for j in range(1,n):
            tsp += u[i]+X[i,j] <= u[j] + (n-1)*(1-X[i,j])
    
    #Resolution
    obj=tsp.solve()
    return (obj, pulp.LpStatus[obj], pulp.value(tsp.objective))

