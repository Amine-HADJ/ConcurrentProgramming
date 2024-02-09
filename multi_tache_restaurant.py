#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    


# Quelques codes d'échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEAREOS = "\x1B[J" # Clear End Of Screen
CLEARELN = "\x1B[2K" # Clear Entire LiNe
CLEARCUP = "\x1B[1J" # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH" # ('H' ou 'f') : Goto at (y,x), voir le code
DELAFCURSOR = "\x1B[K" # effacer après la position du curseur
CRLF = "\r\n" # Retour à la ligne
CURSON = "\x1B[?25h" # Curseur visible
CURSOFF = "\x1B[?25l" # Curseur invisible
# VT100 : Actions sur les caractères affichables
# NORMAL = "\x1B[0m" # Normal
BOLD = "\x1B[1m" # Gras
UNDERLINE = "\x1B[4m" # Souligné
# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m" # Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m" # Rouge 
CL_GREEN="\033[22;32m" # Vert
CL_BROWN = "\033[22;33m" # Brun 
CL_BLUE="\033[22;34m" # Bleu
CL_MAGENTA="\033[22;35m" # Magenta 
CL_CYAN="\033[22;36m" # Cyan
CL_GRAY="\033[22;37m" # Gris
# "01" pour quoi ? (bold ?) 
CL_DARKGRAY="\033[01;30m" # Gris foncé
CL_LIGHTRED="\033[01;31m" # Rouge clair 
CL_LIGHTGREEN="\033[01;32m" # Vert clair
CL_YELLOW="\033[01;33m" # Jaune 
CL_LIGHTBLU= "\033[01;34m" # Bleu clair
CL_LIGHTMAGENTA="\033[01;35m" # Magenta clair 
CL_LIGHTCYAN="\033[01;36m" # Cyan clair
CL_WHITE="\033[01;37m" # Blanc #−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−



# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
    CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='') 
def curseur_invisible() : print(CURSOFF,end='')
def curseur_visible() : print(CURSON,end='')
def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')
def en_couleur(Coul) : print(Coul,end='')
def en_rouge() : print(CL_RED,end='') # Un exemple !







#Importation des modules nécessaires
import sys
import random
import time
import multiprocessing as mp

def client(nb_commandes, queue_commandes, queue_commandes_en_attente, nb_process_serveur, event_client_done):
    """_fonction qui génère les commandes (client)_

    Args:
        nb_commandes (_int_): _nonbre_de commandes_
        queue_commandes (_Queue_): _contient les commandes à envoyer aux serveurs_
        queue_commandes_en_attente (_Queue_): _contient les commandes en attente_
        nb_process_serveur (_int_): _nombre de processus serveur_
        event_client_done (_Event_): _indique si le client a fini de passer ses commandes_
    """
    commandes = [] # Liste des commandes
    for i in range(nb_commandes): # Génère les commandes
        commande = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        commandes.append(commande) # Ajoute la commande à la liste

        #time.sleep(random.randint(1, 2))  # Attente aléatoire entre 1 et 2 secondes

        queue_commandes.put((i+1, commande))  # Envoie de la commande avec l'identifiant client

    for _ in range(nb_process_serveur): # Envoie des commandes en attente
        queue_commandes_en_attente.put(commandes)

  

    
    event_client_done.set() # Signale la fin des commandes

def serveur(num_serveur, queue_commandes, queue_commandes_prete, event_client_done):
    """_fonction qui prépare les commandes (serveurs)_

    Args:
        num_serveur (_int_): _identifiant du serveur_
        queue_commandes (_Queue_): _contient les commandes à traiter_
        queue_commandes_prete (_Queue_): _contient les commandes préparées_
        event_client_done (_Event_): _indique si le client a fini de passer ses commandes_
    """
    while not event_client_done.is_set() or not queue_commandes.empty(): # Tant que le client n'a pas fini ou qu'il reste des commandes à traiter
        
        if not queue_commandes.empty(): # Si il y a des commandes à traiter
            
            commande_a_preparer = queue_commandes.get() # Récupère la commande
            time.sleep(random.randint(3, 5)) # Préparation de la commande
            queue_commandes_prete.put((num_serveur, commande_a_preparer)) # Envoie de la commande préparée avec l'identifiant du serveur


def MJ(queue_commandes_prete, queue_commandes_en_attente, event_client_done):
    """_fonction majord'homme qui gère l'affichage des commandes_

    Args:
        queue_commandes_prete (_Queue_): _contient les commandes préparées_
        queue_commandes_en_attente (_Queue_): _contient les commandes en attente_
        event_client_done (_Event_): _indique si le client a fini de passer ses commandes_
    """
    commandes_en_attente = queue_commandes_en_attente.get() # Récupère les commandes en attente

    while not event_client_done.is_set() or commandes_en_attente!=[]: # Tant que le client n'a pas fini ou qu'il reste des commandes en attente
        num_serveur, commande = queue_commandes_prete.get() # Récupère la commande préparée avec l'identifiant du serveur
        if commande[1] in commandes_en_attente: # Si la commande est en attente
            commandes_en_attente.remove(commande[1]) # Supprime la commande des commandes en attente

        effacer_ecran() 
        erase_line_from_beg_to_curs()
        en_couleur(CL_LIGHTBLU)
        move_to(1, 10)
        print('Le serveur', num_serveur, 'traite la commande', commande)
        move_to(2, 10)
        print('Les commandes clients en attente:', commandes_en_attente)
        move_to(3, 10)
        print('Nombre de commandes en attente:', len(commandes_en_attente))
        move_to(4, 10)
        print('Commande', commande[1], 'est servie au client', commande[0], end='\n\n')

        

if __name__ == "__main__":
    import platform 
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
    
    nb_process_serveur = 5 # Nombre de serveurs
    nb_commandes = 20 # Nombre de commandes

    # Création des queues et de l'event
    queue_commandes = mp.Queue() # Contient les commandes à envoyer aux serveurs
    queue_commandes_prete = mp.Queue() # Contient les commandes préparées avec l'identifiant du serveur
    queue_commandes_en_attente = mp.Queue() # Contient les commandes en attente
    event_client_done = mp.Event() # Event qui signale la fin des commandes envoyé par le client

    # Création des processus
    process_client = mp.Process(target=client, args=(nb_commandes, queue_commandes, queue_commandes_en_attente, nb_process_serveur, event_client_done))
    process_serveur = [mp.Process(target=serveur, args=(i+1, queue_commandes, queue_commandes_prete, event_client_done)) for i in range(nb_process_serveur)]
    process_MJ = mp.Process(target=MJ, args=(queue_commandes_prete, queue_commandes_en_attente, event_client_done))

    # Lancement des processus
    process_client.start()
    for serv in process_serveur:
        serv.start()
    process_MJ.start()

    # Attente de la fin des processus
    process_client.join()
    for serv in process_serveur:
        serv.join()
    process_MJ.join()
    
    # Affichage de fin
    move_to(7, 10)
    en_couleur(CL_LIGHTRED)
    print('Toutes les commandes ont été servies, les serveurs ont bien mérité leur pause!')
    move_to(8, 10) 
    print('Bon Appétit!!')
    
    sys.exit(0) #Fin du programme
