#!/usr/bin/env python3

#############################       REALISÉ PAR 
#############################       HADJ-HAMDRI MOHAMMED-AMINE
#############################       EL-ALAOUI YOUNESS
#############################       3 ETI       GRP-D   2023

import sys
import multiprocessing as mp
import time, random

#Fonctions
def controleur():
  """Fonction de contrôle de la température et de la pression"""
  while True:
      with verrou:
          T=mem_T.value
          P=mem_P.value

      # Temperature
      if T<seuil_T:
        go_chauffage.value=True
      else : 
        go_chauffage.value=False

      # Pression
      if P<seuil_P:
          go_pompe.value=True
      else:
          go_pompe.value=False

      time.sleep(1)
   
def chauffage(go_chauffage):
  """ Etat du chauffage"""
  while True:
      if go_chauffage.value:
          print("Chauffage est allumé")
      else:
          print("Chauffage est éteint")
      time.sleep(1)

def temperature(valeurcapteur):
  """Fonction de variation de la température en fonction de l'état du chauffage"""
  V = valeurcapteur
  while True:
      # Variation de la température en fonction de l'état du chauffage
      if go_chauffage.value :
         V += 0.5
      else : 
        val = random.randint(0,2)
        if val > 0 :
            V += 0.2
        else:
            V -= 0.2
      T = V
      # Ecriture de la température dans la mémoire partagée
      with verrou:
          mem_T.value = T
      time.sleep(1)
      V = T

def pression(valeurcapteur):
  """Fonction de variation de la pression en fonction de l'état de la pompe"""
  
  V = valeurcapteur
  
  while True:
      # Variation de la pression en fonction de l'état de la pompe
      if go_pompe.value :
          V += 0.1
      else : 
        val=random.randint(0,2)
        if val > 0 :
            V += 0.05
        else:
            V -= 0.05
      P = V
      # Ecriture de la pression dans la mémoire partagée
      with verrou:
          mem_P.value=P
      time.sleep(1)
      V = P

def pompe(go_pompe):
  """ Etat de la pompe"""
  while True:
      if go_pompe.value:
          print("Pompe est allumé")
      else:
          print("Pompe est éteinte")
      time.sleep(1)

def ecran():
  """Lecture et Affichage des variables partagées"""
  while True:
      #Lecture des variables partagées
      with verrou:
          T=mem_T.value
          P=mem_P.value
          etat_chauffage=go_chauffage.value
          etat_pompe=go_pompe.value
    # Affichage des variables partagées
      print("T %6.2f"%(T))
      print("P %6.2f"%(P))
      print("Chauffage : {}".format(etat_chauffage))
      print("Pompe : {}".format(etat_pompe),end='\n\n')

      time.sleep(1)


#Programme principal
if __name__ == '__main__':
    import platform
    
    if platform.system() == "Darwin" :
        
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
    #Déclarations des variables partagées et des verrous
    verrou = mp.Lock()
    seuil_T, seuil_P = 25, 1
    go_pompe = mp.Value('b',False)
    go_chauffage = mp.Value('b',False)
    mem_T = mp.Value('f',0) #mémoire partagée 
    mem_P = mp.Value('f',0) #mémoire partagée

    #Création des processus
    p1 = mp.Process(target=controleur)
    p2 = mp.Process(target=chauffage,args=(go_chauffage,))
    p3 = mp.Process(target=temperature,args=(20,))
    p4 = mp.Process(target=pression,args=(0.5,))
    p5 = mp.Process(target=pompe,args=(go_pompe,))
    p6 = mp.Process(target=ecran)

    #Démarrage des processus
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    #Attente de la fin des processus
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    
    #Fin du programme
    print("Fin du programme")
    sys.exit(0)