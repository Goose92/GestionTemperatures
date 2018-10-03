# GestionTemperatures
Cette application permet de relever réguliement des températures via une sonde DALLAS sur un raspberry.

Exemple de lancement de l'application :
python Main.py PROD 1 60
=> Cela lance le script en boucle infinie (prod), en utilisant la sonde 1 dans firebase avec un relevé toutes les 60 minutes.
Il faut lancer le programme avec ces 3 paramètres :
1 : PROD ou Test
2 : le numero de la sonde dans firebase
3 : Le nombre de minutes entre chaque itération.

Avant de lancer le programme, il faut configurer la RPI pour qu'elle puisse dialoguer avec la sonde
# Via un sudo vi /etc/modules, Ajouter ceci dans le fichier /etc/modules :
# w1-gpio
# w1-therm
# Puis rebooter le RPI
# Ajouter dans le /boot/config.txt (toujours avec sudo)
# dtoverlay=w1-gpio
# La temperature se trouve ensuite dans un fichier qui se trouve dans /sys/bus/w1/devices/
# Puis dans un fichier qui commence par 28

La configuration de la base firebase est la suivante (exemple avec 2 sondes):

temperature
  1
    Date
    Libellé
    valeur
  2
    Date
    Libellé
    valeur


Il faut également créer un fichier VariablesConfig.py, et indiquer la valeur de la base firebase que vous utilisez (comme dans le fichier VariablesConfig.py.Example)
CompteFirebase='https://Nom-xxxxx.firebaseio.com/'
