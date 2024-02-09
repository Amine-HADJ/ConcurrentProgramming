#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    

import multiprocessing as mp
import random, sys

def demandeur(queue, nb_operateurs) :
    """_fonction demandeur qui génère les demandes_

    Args:
        queue (_queue_): _file d'attente des demandes_
        nb_operateurs (_int_): _nombre d'opérateurs_
    """
    demande = []  #Liste des demandes
    
    for i in range(nb_operateurs): #Création des demandes
        nb1 = random.randint(1,10) 
        nb2 = random.randint(1,10)
        operation = random.choice(['+', '-', '*', '/'])
        demande.append((str(nb1) + operation + str(nb2))) #Ajoute la demande à la liste
        print("Le demandeur a envoyé ", demande[i]," à l'opérateur ", i+1) #Affiche la demande envoyée
    queue.put(demande) #Envoie la liste des demandes dans la queue
  

        
def calculateur(calcul, i, fil_dattente_des_resultats):
    """_fonction qui calcule les demandes_

    Args:
        calcul (_str_): _demande à calculer_
        i (_int_): _numéro de la demande_
        fil_dattente_des_resultats (_queue_): _file d'attente des résultats_
    """
    
    print("L'opérateur ", i+1, " a reçu ", calcul[i]) #Affiche la demande reçue
    print("le résultat de la demande", i+1, "est :", eval(calcul[i]), end="\n\n") #Affiche le résultat de la demande
    fil_dattente_des_resultats.put(eval(calcul[i])) #Envoie le résultat dans la file d'attente des résultats
    

if __name__ == "__main__" :
    
    import platform
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    queue = mp.Queue() #Création de la queue
    fil_dattente_des_resultats = mp.Queue() #Création de la file d'attente des résultats
    nb_operateurs = 5 
    process_demandeur = mp.Process(target=demandeur, args=(queue,nb_operateurs)) #Création du process demandeur
    process_demandeur.start()
    process_demandeur.join()
    
    operateurs = [0 for i in range(nb_operateurs)] #Création de la liste des process opérateurs
    
    calcul = queue.get() #Récupération des demandes dans la queue
    
    for i in range(nb_operateurs): #Création des process opérateurs, démarrage et attente de la fin de chaque process
        operateurs[i] = mp.Process(target=calculateur, args=(calcul,i,fil_dattente_des_resultats) )
        operateurs[i].start()
        operateurs[i].join()

    
  
        
    resultats_finaux = []
    
    while not fil_dattente_des_resultats.empty(): #Récupération des résultats dans la file d'attente des résultats
        resultat = fil_dattente_des_resultats.get()
        resultats_finaux.append(resultat)
    
    print("Les résultats sont :", resultats_finaux)
    
    sys.exit(0) # Fin du programme
    
    
    
# Pour vérifier la justesse de l’expression, on peut vérifier la syntaxe de l'expression en parcourant la chaîne de caractères de chaque demande.
# La chaine de caractère doit commencer et finir par un nb. Les nbs doivents etre séparer par un opérateur

#Par exemple: 
# if not calcul[i][0].isdigit() or not expression[i][-1].isdigit():
#         return False
    
#     # Vérifier si les nombres et les opérateurs sont alternés
#     for j in range(1, len(calcul[i])-1, 2):
#         if not calcul[i][j] in ['+', '-', '*', '/']:
#             return False