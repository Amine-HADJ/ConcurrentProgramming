#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    


import multiprocessing as mp
import math, sys
import numpy as np



def calcul(queue, sem, l):
    """_summary_

    Args:
        queue (_Queue_): Queue dans laquelle on va mettre le résultat
        sem (_Semaphore_): Sémaphore pour éviter les conflits d'accès à la queue
        l (_list_): Sous-liste de la liste des valeurs de l'abscisse (liste)
    """
    resultat = 0 #Variable locale
    
    for i in l: #Calcul de la somme
        resultat += math.sqrt(1 - i**2)
    sem.acquire() #Protection de la queue
    queue.put(resultat) #Ajout du résultat dans la queue
    sem.release() #Libération de la queue






if __name__ == "__main__" :
    
    import platform
    
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
        
    nb_de_process = 8
    nb_valeurs_N = 1000000
    resultat_final = 0
    liste = np.linspace(0, 1, nb_valeurs_N) #Création de la liste des valeurs de l'abscisse
    taille_sous_liste = ((len(liste)) + nb_de_process - 1) // nb_de_process  # Calcul de la taille approximative de chaque sous-liste
    sous_listes = [liste[i:i + taille_sous_liste] for i in range(0, len(liste), taille_sous_liste)]

    queue = mp.Queue() #Création de la queue
    processus=[0 for i in range(nb_de_process)] #Création d'un tableau de processus
    sem = mp.Semaphore(1) #Création du sémaphore

    for i in range(nb_de_process): #Création des process et affectation de la queue, du sem et de la sous-liste
        process = mp.Process(target=calcul, args=(queue,sem, sous_listes[i]))
        processus[i] = process
        process.start()
        
    for i in range(nb_de_process): #Attente de la fin des processus
        processus[i].join()
        
    for i in range(nb_de_process): #Récupération des résultats
        resultat_final += queue.get()
       
    print("La valeur calculée de pi est la suivante", resultat_final / nb_valeurs_N * 4) #Affichage du résultat
    print("Cette valeur a été calculée par", nb_de_process, "processus, pour", nb_valeurs_N, "valeurs de l'abscisse.") #Affichage des paramètres de calcul
    
    sys.exit(0) #Fin du programme