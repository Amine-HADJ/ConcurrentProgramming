#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023
                                    

# Course Hippique (version élèves)
# Version très basique, sans mutex sur l'écran, sans arbitre, sans annoncer le gagnant, ... ...
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− # VT100 : Actions sur le curseur
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


import multiprocessing as mp
import os, time,math, random, sys, ctypes



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

# La tache d'un cheval
#Fonction cheval qui gère le déplacement d'un cheval
def un_cheval(ma_ligne : int, keep_running,positions,sem) : 
    """_summary_

    Args:
        ma_ligne (int): position du cheval au depart
        keep_running : Flag pour arreter les processus
        positions (_list_): contient la position de chaque cheval
        sem (_Sem_): Sémaphore pour protéger la variable partagée
    """
    col=1     # ma_ligne commence à 0
    while col < LONGEUR_COURSE and keep_running.value : 
        move_to(ma_ligne+1,col) # pour effacer toute ma ligne
        erase_line_from_beg_to_curs() 
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('('+chr(ord('A')+ma_ligne)+'>')
        col+=1
        time.sleep(0.1 * random.randint(1,5))
        sem.acquire() # On protège la variable partagée
        positions[ma_ligne]=col
        sem.release() # On libère la variable partagée
        
#FONCTION ARBITRE
def arbitre(keep_running,positions,sem):
    """_summary_

    Args:
        positions (_list_): contient la position de chaque cheval
        sem (Sem): Sémaphore pour protéger la variable partagée
    """
    
    while keep_running.value and min(positions)<LONGEUR_COURSE-1:
        sem.acquire() # On protège la variable partagée
        move_to(Nb_process+5, 10)
        erase_line_from_beg_to_curs()
        en_couleur(CL_RED)
        cheval_en_tete = positions[:].index(max(positions)) # On fait une copie de la liste pour ne pas modifier la liste originale
        cheval_en_tete = chr(ord('A')+cheval_en_tete) # On convertit l'indice en lettre
        print('LE PREMIER EST : ', cheval_en_tete) # On affiche le cheval en tête
        
        move_to(Nb_process+6, 10)
        erase_line_from_beg_to_curs()
        en_couleur(CL_RED)
        cheval_en_queue = positions[:].index(min(positions)) # On fait une copie de la liste pour ne pas modifier la liste originale
        cheval_en_queue = chr(ord('A')+cheval_en_queue) # On convertit l'indice en lettre
        print('LE DERNIER EST : ', cheval_en_queue) # On affiche le cheval en queue
        sem.release() # On libère la variable partagée
        
    
    
    
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− # La partie principale :
if __name__ == "__main__" :

    pronostic = input("Quel est votre pronostic ? (entrez la lettre du cheval) : ") # On demande le pronostic avant le début de la course
    
    import platform
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    
            
    LONGEUR_COURSE = 100 # Tout le monde aura la même copie (donc no need to have a 'value')
    keep_running=mp.Value(ctypes.c_bool, True)
    # course_hippique(keep_running)
    
    Nb_process = 26 # Nombre de chevaux
    mes_process = [0 for i in range(Nb_process)] # Une liste pour stocker les processus
    
    positions = mp.Array(ctypes.c_int, Nb_process) # Une liste partagée pour les positions
    sem = mp.Semaphore(1) # Un sémaphore pour protéger les accès à la liste des positions
    effacer_ecran()
    curseur_invisible() 
    
    for i in range(Nb_process): # Lancements des processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,positions,sem))
        mes_process[i].start()
        
    move_to(Nb_process+10, 1)
    print("tous lancés")
    move_to(Nb_process+11, 1)
    print("Votre pronostic est : ", pronostic.upper())
    
        
    
    process_arbitre = mp.Process(target=arbitre, args= (keep_running,positions,sem)) # Création du processus arbitre
    process_arbitre.start() # Lancement du processus arbitre
    
    
    for i in range(Nb_process):
        mes_process[i].join() # Attendre la fin des processus
    
    process_arbitre.join() # Attendre la fin du processus arbitre
    
    # On affiche le résultat
    cheval_en_tete = positions[:].index(max(positions))
    cheval_en_tete = chr(ord('A')+cheval_en_tete)
    move_to(Nb_process+15, 1)
    
    
    
    if pronostic.upper() == cheval_en_tete: # On compare le pronostic avec le cheval en tête
        print("Vous avez gagné, votre cheval est arrivé premier!")
        time.sleep(3)
    else:
        print("Vous avez perdu, votre cheval n'est pas arrivé premier, c'est le cheval:", positions[-1])
        time.sleep(3)
    
    move_to(24, 1)
    curseur_visible() 
    print("Fini")
    
    sys.exit(0) # Fin de programme