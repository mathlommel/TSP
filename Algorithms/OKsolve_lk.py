import numpy as np


def solve_lk(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M by using the
    Lin–Kernighan heuristic.

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
    
    route=np.arange(n)
    route=np.concatenate((route,0),axis=None)
    coutRoute=np.sum(M[route[i],route[i+1]] for i in range(0,n))
    
    tauxAmelioration=0.05
    diff=1
    
    while diff > tauxAmelioration:
        
        coutaBattre=coutRoute
        
        for i in range(1,n-1):
            for j in range(i+1,n):
                nvRoute=np.concatenate((route[0:i],route[j:-n+i-2:-1],route[j+1:n]),axis=None)
                nvRoute=np.concatenate((nvRoute,0),axis=None)
                
                nvCout=np.sum(M[nvRoute[k],nvRoute[k+1]] for k in range(0,n))
                
                if (nvCout<coutRoute):
                    route=nvRoute.copy()
                    coutRoute=nvCout
                
        diff=1-coutRoute/coutaBattre
    
    return coutRoute
