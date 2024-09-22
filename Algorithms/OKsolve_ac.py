import numpy as np

def solve_ac(M):
    """
    Solves the TSP instance encoded in the adjacency matrix M using an
    Ant-Colony heuristic.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.

    Returns
    -------
    cost : int or float
        The solution tour cost.
    """
    #Nombre de villes
    n=len(M[0,:])
    
    #Initialisation du nombre de fourmis par groupe   
    nbFourmiparGrp=n
    #Initialisation du coefficient d'évaporation des phéromones
    rho=0.9
    #Coefficient associé à l'importance des phéromones dans la décision des chemins 
    alpha=0.5
    
    #Matrices utilisées pour les transitions des groupes de fourmis
    Pactif=1/(M+10**-150)            #Matrice du groupe de fourmis n
    Pfutur=Pactif.copy()    #Matrice du groupe de fourmis n+1
    
    #Conservation en mémoire des arcs déjà visités
    arcsVisites=np.zeros((n,n))
    #Valorisation des arcs pas encore parcourus
    gamma=np.min(Pactif)
    
    #Matrice contenant les quantités de  phéromones déposées sur chaque arc
    Phero=np.ones((n,n))
    #Bornes max et min des quantités de phéromones sur chaque arc
    pheroMax=5
    pheroMin=1
    
    #Nb maximal de fourmis à se déplacer (1er critère d'arrêt)
    nbFourmis=10*n
    #2nd critère d'arrêt : lorsque le cout minimal reste inchangé pendant nbStag passages de fourmis
    cpt=0
    nbStag=3*n
    
    #On initialise le cout minimal à l'infini
    minCost=np.inf
    
    #Indice de la fourmi à se déplacer
    i=0
    
    while(i<nbFourmis and cpt<nbStag):
        #On crée une trajectoire au sein du graphe
        traj,cost=createTraj(Pactif,M)
        
        #On actualise éventuellement le meilleur cout, et on réinitialise le compteur
        if (cost<minCost):
            cpt=0
            minCost=cost
        else:
            #Considération du fait que le cout n'a pas été battu par la nouvelle trajectoire
            cpt+=1
        
        #Actualisation de la matrice de transition pour le prochain groupe de fourmis
        for j in range(0,n):
            
            #Cas d'une visite d'arc jamais visité encore
            if arcsVisites[traj[j],traj[j+1]]==0:
                arcsVisites[traj[j],traj[j+1]]=1
                arcsVisites[traj[j+1],traj[j]]=1
                #Modification symétrique de la matrice de transition
                Pfutur[traj[j],traj[j+1]]+=gamma
                Pfutur[traj[j+1],traj[j]]+=gamma
            
            #Coefficient associé à l'incrémentation linéaire de la quantité de phéromones
            Q=n*minCost/cost
            
            #Dépot de phéromones sur l'arc 
            Phero[traj[j],traj[j+1]]=min(rho*(Phero[traj[j],traj[j+1]]+Q/M[traj[j],traj[j+1]]),pheroMax)
            Phero[traj[j+1],traj[j]]=min(rho*(Phero[traj[j+1],traj[j]]+Q/M[traj[j+1],traj[j]]),pheroMax)
            #Evaporation des phéromones
            Phero[traj[j],traj[j+1]]=max(Phero[traj[j],traj[j+1]],pheroMin)
            Phero[traj[j+1],traj[j]]=max(Phero[traj[j+1],traj[j]],pheroMin)
            
            #Mise à jour de P après passage du groupe de fourmis
            if (i%nbFourmiparGrp==0):
                Pfutur=(Pfutur)*(Phero**alpha)
                Pactif=Pfutur.copy()
        i+=1
    
    return (minCost)


def createTraj(P,M):
    """
    Creates a trajectory between the cities of the graph, considering a transition matrix P.
    The trajectories will be obtain by a random choice, using a Uniform Law.

    Arguments
    ---------
    M : np.ndarray
        The adjacency matrix.
    P : np.ndarray
        The transition matrix.

    Returns
    -------
    traj : np.array
        The trajectory generated.
    cost : int
        The cost of the trajectory created.
    """
    
    #Etats Disponibles
    nbEtats=len(P[0,:])
    etatsDispo=np.linspace(0,nbEtats-1,nbEtats,dtype=int)
    
    #Initialisation d'une trajectoire vide
    traj=np.zeros(nbEtats+1,dtype=int)
    
    #On retire l'état initial des états pouvant être parcourus
    etatsDispo=np.delete(etatsDispo,0)
    #On initialise le cout de la trajectoire
    cost=0    
    
    #Vecteur x tel que x_i=0 si la ville a déjà été visitée, et x_i=1 sinon
    x=np.ones(nbEtats,dtype=int)
    
    #Création de la trajectoire
    for i in range(1,nbEtats):
        #On retire l'état précédemment visité : on met un 0 dans x à l'indice correspondant
        x[traj[i-1]]=0
        
        #Choix aléatoire d'un nouvel état de manière uniforme 
        vectProba=P[traj[i-1],(x==1)]/np.sum(P[traj[i-1],(x==1)])
        traj[i]=np.random.choice(etatsDispo, size=1, replace=True, p=vectProba)
        
        #On retire l'état choisi des états encore disponibles
        etatsDispo=np.delete(etatsDispo,np.where(etatsDispo==traj[i]))
        
        #On modifie le cout global de la trajectoire en conséquence
        cost+=M[traj[i-1],traj[i]]
    
    #On ajoute la ville de départ en fin de trajectoire
    traj=np.concatenate((traj,0),axis=None)
    #On incrémente le cout global
    cost+=M[traj[nbEtats-1],traj[nbEtats]]
    
    return (traj,cost)

    
