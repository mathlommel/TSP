import itertools
import numpy as np
import pulp

def solve_dfj(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M by solving its
    Dantzig–Fulkerson–Johnson formulation.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.

    Returns
    -------
    cost : int or float
        The solution tour cost.
        
        if (i>=2):
            for Q in itertools.combinations(range(1, n), i):
                tsp += pulp.lpSum(X[k,l] for k in Q for l in Q if (l!=k))<=i-1
        
    """
    n=len(M[0,:])
    
    #Définition du problème
    tsp=pulp.LpProblem("TSP",sense=pulp.LpMinimize)
    
    #Variable de décision
    X = pulp.LpVariable.dicts("X",((i,j) for i in range(0,n) for j in range(0,n)), lowBound=0, upBound=1,cat='Binary')
    #Fonction à maximiser
    tsp += pulp.lpSum([X[i,j]*M[i,j] for i in range(0,n) for j in range(0,n)])
    
    #Contraintes
    for i in range(0,n):
        tsp += X[i,i]==0
        tsp += pulp.lpSum([X[i,j] for j in range(0,n)])==1  #Contrainte sur les lignes de X
        tsp += pulp.lpSum([X[j,i] for j in range(0,n)])==1  #Contrainte sur les colonnes de X
        
    
    test=True

    while(test):
        #Resolution
        obj=tsp.solve()
        cpCnx=composantes_Connexes(n,X)
        
        if len(cpCnx)!=1:
            for key in cpCnx.keys():
                tsp += pulp.lpSum(X[k,l] for k in cpCnx[key] for l in cpCnx[key])<=len(cpCnx[key])-1
            
        else:
            test=False
    
    return (obj, pulp.LpStatus[obj], pulp.value(tsp.objective))

def composantes_Connexes(N,X):
    numbers = np.arange(N)
    
    #Tant que des modifications sont possibles, on assigne une même valeur aux éléments 
    #   appartenant à une même composantes connexe
    modifications = True
    while modifications:
        #Si une itération complète n'entraine pas de modification : fin
        modifications = False
        for i in range(N):
            for j in range(N):
                if pulp.value(X[i, j]) == 1 and numbers[i] != numbers[j]:
                    numbers[i] = numbers[j] = min(numbers[i], numbers[j])
                    modifications = True
    
    #On va d"sormais placer dans un même ensemble les villes ayant la même valeur attribuée
    res = {}
    for i, c in enumerate(numbers):
        if c not in res:
            res[c] = []
        res[c].append(i)
                
    return res
