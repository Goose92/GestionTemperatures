
import os
import sys
import glob
import time
import datetime
import random
import urllib

import ModuleGestionConnexion # Import des fonctions permettant de tester la connexion internet
from VariablesConfig import CompteFirebase # Import du fichier de config

from firebase import firebase

# Initionalisation du systeme de gestion
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Initialisation de la variable permettant de trouver le fichier ou est stocke la temperature via la sonde DALLAS
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

TableauBuffer = [] # Creation du tableau qui sert de buffer si internert est off

# Fonction pour lire le contenu du fichier des temperatures
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Fonction pour lire le contenu et l'analyser pour trouver la valeur de la temperature
def read_temp():
    lines = read_temp_raw()
    # Si le fichier ne contient paqs le mot YES, c'est qu'il y a un probleme, on retourne alors -200
    if lines[0].strip()[-3:] != 'YES':
        return -200
    equals_pos = lines[1].find('t=')  # On regarde la position du mot t= dans la seconde ligne du fichier
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 100.0
        return int(temp_c)


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
