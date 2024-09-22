import numpy as np
import itertools

def solve_hk(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M by using the
    Held-Karp algorithm.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.

    Returns
    -------
    cost : int or float
        The solution tour cost.
        
    """
    #Récupération des dimensions de la matrice M (nombre de noeuds)
    n=len(M[0])
    
    #Initialisation du dictionnaire g(subset, noeud)
    g={}
    for k in range(1,n):
        g[(k,),k]=M[0,k]
    
    #Ajout des données au dictionnaire créé
    for s in range(2,n):
        #Pour tout ensemble de sommets de taille s
        for subset in itertools.combinations(range(1, n), s):
            #Recherche du chemin de cout minimal de 0 à k passant par le subset
            for k in subset:
                valMin=np.inf
                #On crée un subset en retirant k
                sub=list(subset)
                sub.remove(k)
                subsetK=tuple(sub)
                
                #Optimisation ??
                #for m in subset:
                #    if m!=k:
                #        val=g[subsetK,m]+M[m,k]
                #        
                #        if val < valMin:
                #            valMin=val
                #Optmisation
                vect=[]
                for m in subset:
                    if m!=k:
                        vect.append(g[subsetK,m]+M[m,k])
                g[subset,k]=min(vect)
                
                #g[subset,k]=valMin
                
    #Idem ??
    opt=np.inf
    s=tuple(np.arange(1,n))
    res=[]
    #for k in range(1,n):
    #    val=g[s,k]+M[k,1]
    #    if val<opt:
    #        opt=val
    for k in range(1,n):
        res.append(g[s,k]+M[k,0])
    
    opt=min(res)
    return (opt)
                
