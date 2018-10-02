# GestionTemperatures
Système de gestion de températures via Python / sonde DALLAS / Raspberry

# Programme permettant de relever regulierement la temperature d'une sonde DALLAS et de l'envoyer sur Firebase
# Via un sudo vi /etc/modules, Ajouter ceci dans le fichier /etc/modules :
# w1-gpio
# w1-therm
# Puis rebooter le RPI
# Ajouter dans le /boot/config.txt (toujours avec sudo)
# dtoverlay=w1-gpio
# La temperature se trouve ensuite dans un fichier qui se trouve dans /sys/bus/w1/devices/
# Puis dans un fichier qui commence par 28
