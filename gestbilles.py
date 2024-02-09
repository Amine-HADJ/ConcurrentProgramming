#!/usr/bin/env python3

#############################       REALISÃ‰ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023

import sys
import multiprocessing as mp
import time


def demander_ressources(k_bills, semaphore,nbr_disponible_billes):
    while True:
        # Acquérir le sémaphore pour entrer dans la section critique
        semaphore.acquire()  
        if nbr_disponible_billes.value >= k_bills:
            nbr_disponible_billes.value -= k_bills
            # Libérer le sémaphore après avoir effectué la demande
            semaphore.release()  
            break
        else:
            # Libérer le sémaphore avant de se mettre en attente
            semaphore.release()  
            """Ajouter une variable partagée pour compter le nombre de travailleurs bloqués"""

            



def rendre_ressources(k_bills, semaphore,nbr_disponible_billes):
    # Acquérir le sémaphore pour entrer dans la section critique
    semaphore.acquire()  
    nbr_disponible_billes.value += k_bills
    # Libérer le sémaphore après avoir effectué le rendu
    semaphore.release()  
    for _ in range(k_bills):#il faudra changer le k_bills en un autre nombre comme ca on aura pas un exces de jetons
        # Libérer les travailleurs bloqués sur demander_ressources
        semaphore.release()  


def travailleur(semaphore,nbr_disponible_billes,k):
    for _ in range(2):#m=5
        # Nombre de billes restantes
        print("Travailleur {} : nombre de billes restantes = {}".format(mp.current_process().name, nbr_disponible_billes.value))
        
        # Demander k_bills
        demander_ressources(k, semaphore,nbr_disponible_billes)
        # Simuler le travail avec un délai
        print("Travailleur {} : travaille pendant 1 seconde".format(mp.current_process().name) )
        time.sleep(1)  
        # Rendre k_bills
        rendre_ressources(k, semaphore,nbr_disponible_billes)
        #nombre de billes disponibles




def controleur(max_billes,semaphore,nbr_disponible_billes):
    while True:
        with semaphore:
            if not (0 <= nbr_disponible_billes.value <= max_billes):
                print("nombre de billes épuisé")

        time.sleep(1)  


if __name__ == '__main__':
    import platform
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    # Nombre maximum de billes disponibles
    nb_max_billes = 9
    # Nombre de billes disponibles
    nbr_disponible_billes = mp.Value('i', nb_max_billes)  
    # Nombre de billes nécessaires pour chaque processus (P1, P2, P3, P4)
    k = [4, 3, 5, 2]  
    # Sémaphore pour contrôler l'accès à la ressource
    semaphore = mp.Semaphore(nb_max_billes)  
    # Créer 4 processus travailleurs
    travailleurs = [mp.Process(target=travailleur, args=(semaphore,nbr_disponible_billes,k[i])) for i in range(4)]
    # Lancer les 4 processus travailleurs
    for travailleur_ in travailleurs:
        travailleur_.start()
    # Créer un processus contrôleur
    controleur_process = mp.Process(target=controleur, args=(nb_max_billes,semaphore,nbr_disponible_billes))
    # Lancer le processus contrôleur
    controleur_process.start()
    # Attendre la fin des 4 processus travailleurs
    for travailleur_ in travailleurs:
        travailleur_.join()
    # Terminer le processus contrôleur
    controleur_process.terminate()
    sys.exit(0)