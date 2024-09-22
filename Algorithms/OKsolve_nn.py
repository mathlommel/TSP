import numpy as np


def solve_nn(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M by using a
    Nearest-Neighbor heuristic.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.

    Returns
    -------
    cost : int or float
        The solution tour cost.
    """
    #Number of cities
    n=len(M[0,:])
    
    #Initialisation du cout minimal
    cost=0
    #On crée un vecteur qui contiendra les couts des trajectoires obtenues pour un départ dans chaque ville possible
    costAll=np.zeros(n)
    
    #On teste avec un départ dans chaque ville possible, et on applique l'heuristique
    for k in range(0,n):
        #Initialisation des variables contenant chaque couple de ville à suivre
        villePrec=k
        villeFuture=k
        
        #On garde en mémoire les villes visitées (x_i=0 si visitée, x_i=1 sinon)
        x=np.ones(n,dtype=int)
        
        for i in range(1,n):
            #Considération de la ville déjà visitée
            x[villePrec]=0
            
            #On choisit le plus proche voisin pas encore visité
            villeFuture=np.argwhere(M[villePrec,:]==np.min(M[villePrec,(x==1)]))[0,0]
            
            cost += M[villePrec,villeFuture]
            villePrec=villeFuture.copy()
        
        #On retourne à notre ville initiale
        villeFuture=k
        #On ajoute le cout correspondant
        cost+= M[villePrec,villeFuture]
        
        #On ajoute le cout de cette trajectoire au vecteur contenant tous les couts
        costAll[k]=cost
        #On réinitialise le cout à 0
        cost=0
        
    return (min(costAll))
