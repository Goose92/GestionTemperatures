
import os
import sys
import glob
import time
import datetime
import random
import urllib

import ModuleGestionConnexion # Import des fonctions permettant de tester la connexion internet
from VariablesConfig import CompteFirebase # Import du fichier de config
import GestionSonde # Import du module de gestion de la sonde Dallas
from firebase import firebase

# Initionalisation du systeme de gestion
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')



def AjouterItemBuffer(Item) :
    TableauBuffer.append(Item)

def SupprimerVieilleValeurBuffer() :
    del TableauBuffer[0]

def LirePlusVieilleValeurBuffer() :
    return TableauBuffer[0]

def ViderBuffer() :
    while len(TableauBuffer)>0 :
      PlusVieilleValeur=LirePlusVieilleValeurBuffer()
      print(PlusVieilleValeur)
      # Mettre ici la fonction pour enregistrer ou je veux la valeur
      del TableauBuffer[0]

# ------------------------------------------------
# Debut du programme principal

if len(sys.argv) == 2 : # Il faut qu'il y ait un argument et un seul (le num pour firebase)
	Chaine=sys.argv[1]
	if Chaine.isdigit() :
   		x = int(Chaine)
    	print(Chaine,"Lancement de l'application correct (un seul argument)")
        # On rentre dans la boucle infinie
        firebase = firebase.FirebaseApplication(CompteFirebase,None)
        Interval=60*60  # Temps en seconde entre chaque verification
        Cpt=0
        while 1 == 1 :
            ValTemp=read_temp() # On recupere la temperature actuelle
            Horodatage=datetime.datetime.now()
            if InternetOk()==True :   # On regarde si internet est up
                # On peut deposer la valeur dans firebase (mais aussi dans la BdD)
                ViderBuffer()   # On commence par profiter pour vider le buffer
                VariableFirebase="/Temperature/" + Chaine
                print(VariableFirebase)
                firebase.put(VariableFirebase,'Valeur',ValTemp)
                firebase.put(VariableFirebase,'Date',Horodatage)
                print("Internet OK",ValTemp,Horodatage)
            else :
                # On ne peut pas deposer dans firebase, on stocke dans le buffer pour plus tard
                AjouterItemBuffer([ValTemp,Horodatage])
                print("Internet OFF",ValTemp,Horodatage)
            Cpt=Cpt +1
            time.sleep(Interval)
	else :
        	print(Chaine,"Echec : Il faut un argument numerique pour indiquer le numero de la sonde")
else :
	print("Echec : Il faut un argument numerique et un seul pour indiquer le numero de la sonde")
