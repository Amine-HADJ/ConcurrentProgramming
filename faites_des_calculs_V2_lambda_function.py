#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    


import multiprocessing as mp
import random, sys, time, math


# FONCTIONS

def demandeur(queue, i, sem, functions):
    """_fonction qui génère les demandes (demandeurs)_

    Args:
        queue (_str_): _demande n°i_
        i (_int_): _numéro de la demande_
        sem (_semaphore_): _sémaphore pour éviter les conflits d'accès à la queue_
        functions (_dict_): _dictionnaire contenant les fonctions_
    """
    sem.acquire() #On bloque l'accès à la queue
    demande = random.choice(list(functions.keys())) #On choisit une fonction au hasard
    print("Le demandeur", i + 1, "a envoyé la fonction", demande, "à l'opérateur", i + 1) #On affiche la demande envoyée
    queue.put(demande) #On ajoute la demande à la queue
    sem.release() #On libère l'accès à la queue

    time.sleep(0.5) #On attend 0.5s pour laisser le calculateur faire son travail
    
    sem.acquire() #On bloque l'accès à la queue
    resultat = queue.get() #On récupère le résultat de la queue
    print("Le demandeur", i + 1, "a reçu le résultat", resultat, "de l'opérateur", i + 1, end="\n\n") #On affiche le résultat
    sem.release() #On libère l'accès à la queue
    
    

def calculateur(queue, i, sem,functions):
    """_fonction qui calcule les demandes (opérateurs)_
    
    Args:
        queue (_str_): _demande n°i_
        i (_int_): _numéro de la demande_
        sem (_semaphore_): _sémaphore pour éviter les conflits d'accès à la queue_
        functions (_dict_): _dictionnaire contenant les fonctions_
    """
    sem.acquire() #On bloque l'accès à la queue
    fonction = queue.get() #On récupère la fonction à calculer

    x = random.randint(1, 10) #On choisit un nombre au hasard entre 1 et 10
    print("L'opérateur", i+1, "a reçu la fonction", fonction, "et va la calculer pour x =", x) #On affiche la fonction et le nombre choisi
    
    resultat = functions[fonction](x) #On calcule le résultat
    queue.put(resultat) #On ajoute le résultat à la queue
    print("L'opérateur", i + 1, "a calculé le résultat", resultat, "et l'a transmis au demandeur", i + 1) #On affiche le résultat
    sem.release() #On libère l'accès à la queue
    
    


# PROGRAMME PRINCIPAL

if __name__ == "__main__" :
    
    import platform
    
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
     
    # VARIABLES 
    nb_demandeur_operateur = 5 #Nombre de demandeurs et d'opérateurs
    queues = [] #Liste des queues
    
    
    
    #Dictionnaire de fonctions à utiliser
    functions = {'carre' : lambda x:  x**2, 
        'cube' : lambda x: x**3,
        'racine' : lambda x: math.sqrt(x),
        'expo' : lambda x: math.exp(x),
        'inverse' : lambda x: 1/x,
        'log' : lambda x : math.log(x)}
    
    # PROCESS
    
    for _ in range(nb_demandeur_operateur): #Création des queues
        queues.append(mp.Queue())
        
    for i in range(nb_demandeur_operateur): #Création des process et affectation des queues, sémaphore, et numéro distinct
        sem = mp.Semaphore(1)
        process_demandeur = mp.Process(target=demandeur, args=(queues[i],i , sem, functions))
        process_demandeur.start()
        process_operateur = mp.Process(target=calculateur, args=(queues[i], i, sem, functions))
        process_operateur.start()
        process_demandeur.join()
        process_operateur.join()
        
    
     
    sys.exit(0) #Fin du programme