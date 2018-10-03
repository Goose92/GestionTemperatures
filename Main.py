# Import des modules Python utilises dans le programme
import os,sys,glob,time,datetime,random,urllib
from firebase import firebase

# Import des modules particuliers internes au programme
from ModuleGestionConnexion import InternetOk # Import des fonctions permettant de tester la connexion internet
from VariablesConfig import CompteFirebase # Import du fichier de config (pour les variables)
import GestionSonde # Import du module de gestion de la sonde Dallas
from GestionBuffer import TableauBuffer, AjouterItemBuffer, SupprimerVieilleValeurBuffer, LirePlusVieilleValeurBuffer, ViderBuffer # Import du module de gestion du buffer (en cas de perte du reseau)
from GestionSonde import read_temp

# Initionalisation du systeme de gestion
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

Interval=10  # Temps en seconde entre chaque verification

# ------------------------------------------------
# Debut du programme principal
# ------------------------------------------------

# Il faut qu'il y ait 3 arguments (Prod/Test , NumeroSonde, NbMinIntervale)
if len(sys.argv) != 4 :
	print("Il n'y a pas assez de parametre. Exemple d'utilisation : Python Main.py PROD 1 60")
	exit(0)

print(sys.argv[1],sys.argv[2],sys.argv[3])
ParamTypeLancement=sys.argv[1]
if ParamTypeLancement!="PROD" or ParamTypeLancement!="TEST" :
	print("Le premier parametre doit etre PROD pour un lancement avec boucle infinie ou TEST pour une seule iteration")
	exit(0)
ParamNumSondeFB=sys.argv[2]
if ParamNumSondeFB.isdigit()==False :
	print("Le second parametre doit etre un nombre indiquant le numero de la sonde dans firebase")
	exit(0)
ParamInterval=sys.argv[3]
if ParamInterval.isdigit()==False :
	print("Le Troisieme parametre doit etre un nombre indiquant le nombre de minute entre chaque releve")
	exit(0)

print("C'est bon, on continue",' / ',ParamTypeLancement,' / ', ParamNumSondeFB,' / ' , ParamInterval)

if len(sys.argv) == 2 :
    # A faire : Rajouter le fonctionnement avec un 2eme argument pour Prod (boucle infinie) ou Test (1 repetition) + un 3eme pour l'interval
    Chaine=sys.argv[2]
    if Chaine.isdigit() :
         x = int(Chaine)
         print(Chaine,"Lancement de l'application correct (un seul argument)")
         # On rentre dans la boucle infinie
         firebase = firebase.FirebaseApplication(CompteFirebase,None)
         Cpt=0
         while Cpt < 1 :
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
         # Fin de boucle infinie
    else :
        print(Chaine,"Echec : Il faut un argument numerique pour indiquer le numero de la sonde")
else :
    print("Echec : Il faut un argument numerique et un seul pour indiquer le numero de la sonde")
