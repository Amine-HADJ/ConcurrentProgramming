#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    

import multiprocessing as mp
import random, sys, time



def demandeur(queue, i, sem) : #fonction demandeur qui envoie une demande à un opérateur et attend le résultat de ce dernier
    """_summary_

    Args:
        queue (_str_): _demande n°i_
        i (_int_): _numéro de la demande_
        sem (_semaphore_): _sémaphore pour éviter les conflits d'accès à la queue_
    """
    
    nb1 = random.randint(1,10)
    nb2 = random.randint(1,10)
    operation = random.choice(['+', '-', '*', '/'])
    demande = str(nb1) + operation + str(nb2)
    
    sem.acquire() #Acquisition du sémaphore pour éviter les conflits d'accès à la queue
    queue.put(demande)
    sem.release() #Libération du sémaphore
    print("Le demandeur", i+1, "a envoyé ", demande," à l'opérateur ", i+1)
    
    time.sleep(0.5) #Attendre que le process opérateur ait fini de calculer et renvoyer le résultat
    
    sem.acquire() #Acquisition du sémaphore pour éviter les conflits d'accès à la queue
    print("Le demandeur", i+1, "a reçu le résultat de l'opérateur ", i+1, ":", queue.get(), end="\n\n")
    sem.release() #Libération du sémaphore
    
    

def calculateur(queue, i,sem): #fonction opérateur qui reçoit une demande, calcule le résultat et le renvoie au demandeur
    """_summary_

    Args:
        queue (_str_): _demande n°i_
        i (_int_): _numéro de la demande_
        sem (_semaphore_): _sémaphore pour éviter les conflits d'accès à la queue_
    """
    
    sem.acquire()  #Acquisition du sémaphore pour éviter les conflits d'accès à la queue
    calcul = queue.get()
    queue.put(eval(calcul))
    sem.release() #Libération du sémaphore
    print("L'opérateur ", i+1, " a reçu ", calcul, "et à transmis le résultat au demandeur ", i+1)
    
    
    




if __name__ == "__main__" :
    
    import platform
    
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
        
    nb_demandeur_operateur = 3 #Nombre de demandeurs et d'opérateurs
    queues = [] #Liste des queues
    
    for _ in range(nb_demandeur_operateur): #Création des queues
        queues.append(mp.Queue())
        
    for i in range(nb_demandeur_operateur): #Création des process et affectation des queues, sémaphore, et numéro distinct
        sem = mp.Semaphore(1)
        process_demandeur = mp.Process(target=demandeur, args=(queues[i],i,sem))
        process_demandeur.start()
        process_operateur = mp.Process(target=calculateur, args=(queues[i],i,sem))
        process_operateur.start()
        
    for i in range(nb_demandeur_operateur):
        process_demandeur.join()
        process_operateur.join()
        
     
    sys.exit(0) #Fin du programme
    
    
    
    #