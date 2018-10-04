# Import des modules Python utilises dans le programme
import os,sys,glob,time,datetime,random,urllib
from firebase import firebase

# Import des modules particuliers internes au programme
from ModuleGestionConnexion import InternetOk # Import des fonctions permettant de tester la connexion internet
from VariablesConfig import CompteFirebase # Import du fichier de config (pour les variables)
import GestionSonde # Import du module de gestion de la sonde Dallas
from GestionBuffer import TableauBuffer, AjouterItemBuffer, SupprimerVieilleValeurBuffer, LirePlusVieilleValeurBuffer, ViderBuffer # Import du module de gestion du buffer (en cas de perte du reseau)
from GestionSonde import read_temp


# ------------------------------------------------
# Debut du programme principal
# ------------------------------------------------

# Il faut qu'il y ait 4 arguments (Prod/Test , NumeroSonde, NbMinIntervale)
# Exemple de lancement du programme : python Main.py PROD 1 60 SIMU
if len(sys.argv) != 5 :  # Il doit y avoir 4 parametres plus le nom du programme cela fait 5
	print("Il n'y a pas assez de parametre. Exemple d'utilisation : Python Main.py PROD 1 60")
	exit(0)

ParamTypeLancement=sys.argv[1]
if ParamTypeLancement!="PROD" and ParamTypeLancement!="TEST" :
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

ModeSimulation=sys.argv[4]
if ModeSimulation!="SIMU" and ModeSimulation!="REEL" :
	print("Le 4eme parametre doit etre SIMU pour un lancement simulant la sonde et REEL pour le mode entier")
	exit(0)
if ModeSimulation == "SIMU"  :
	print("Le 4eme parametre doit etre SIMU pour un lancement simulant la sonde et REEL pour le mode entier")
	ParamModeSimu=True
if ModeSimulation == "REEL"  :
	print("Le 4eme parametre doit etre SIMU pour un lancement simulant la sonde et REEL pour le mode entier")
	ParamModeSimu=False
	# Initionalisation du systeme de gestion
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')


print("Lancement de l'application correct (parametres), debut des cycles")
firebase = firebase.FirebaseApplication(CompteFirebase,None)
Boucle=True # Par defaut on est en boucle infinie, seule le parametre TEST peut faire passer a False
Interval=60*int(ParamInterval)  # Temps en seconde entre chaque verification

# On rentre dans la boucle infinie
while Boucle == True  :
	if ParamModeSimu==True :
		ValTemp=123 # On simule une temperature
	else :
		ValTemp=read_temp() # On recupere la temperature actuelle
	Horodatage=datetime.datetime.now()
	if InternetOk()==True :   # On regarde si internet est up
	 # On peut deposer la valeur dans firebase (mais aussi dans la BdD)
	 ViderBuffer()   # On commence par profiter pour vider le buffer
	 VariableFirebase="/Temperature/" + ParamNumSondeFB
	 firebase.put(VariableFirebase,'Valeur',ValTemp)
	 firebase.put(VariableFirebase,'Date',Horodatage)
	 print("Internet OK ",ValTemp,Horodatage)
	else :
	 # On ne peut pas deposer dans firebase, on stocke dans le buffer pour plus tard
	 AjouterItemBuffer([ValTemp,Horodatage])
	 print("Internet OFF ",ValTemp,Horodatage)
	if ParamTypeLancement=="TEST" :  # Si on a lance le programme avec le parametre TEST, on ne fait qu un iteration
		Boucle=False
	time.sleep(Interval)
# Fin de boucle infinie
