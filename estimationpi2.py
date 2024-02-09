#!/usr/bin/env python3

#############################       REALISÃ‰ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023

# Importer les modules nécessaires
import sys
import random
import time
import multiprocessing as mp

# Calculer le nombre de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration,hits):
    count = 0
    for _ in range(nb_iteration):
        x = random.random()
        y = random.random()
        # Si le point est dans le cercle unitaire
        if x**2 + y**2 <= 1:
            count += 1
    # Ajouter le nombre de hits à la variable partagée
    hits.value += count
    return count
    

def frequence_de_hits_pour_n_essais_multi(nb_iteration):
    # Créer une variable partagée pour stocker le nombre total de hits
    hits = mp.Value('i', 0)
    # Calculer le nombre d’itérations qu'il faut par processus
    nb_iteration_par_processus = nb_iteration // mp.cpu_count()
    # Créer les processus
    processus = [mp.Process(target=frequence_de_hits_pour_n_essais, args=(nb_iteration_par_processus, hits))
                 for _ in range(mp.cpu_count())]
    # Lancer les processus
    for p in processus:
        p.start()
    # Attendre la fin de tous les processus
    for p in processus:
        p.join()
    # Récupérer le nombre total de hits à partir de la variable partagée
    nb_hits = hits.value
    # Calculer la valeur estimée de π
    pi_estime = 4 * nb_hits / nb_iteration
    return pi_estime

if __name__ == '__main__':
    
    import platform
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    
    # Nombre d’essais pour l’estimation
    nb_iteration = 10000000
    # Mesurer le temps de calcul pour la méthode Mono-Processus
    start_time = time.time()
    nb_hits = frequence_de_hits_pour_n_essais(nb_iteration, mp.Value('i', 0))
    end_time = time.time()
    print("Valeur estimée de Pi par la méthode Mono-Processus :", 4 * nb_hits / nb_iteration)
    print("Temps de calcul :", end_time - start_time, "secondes")
    # Mesurer le temps de calcul pour la méthode Multi-Processus
    start_time = time.time()
    pi_estime = frequence_de_hits_pour_n_essais_multi(nb_iteration)
    end_time = time.time()
    # Afficher les résultats
    print("Valeur estimée de π par la méthode multi-processus :", pi_estime)
    print("Temps de calcul avec plusieurs processus :", end_time - start_time, "secondes")
    sys.exit(0)


   
