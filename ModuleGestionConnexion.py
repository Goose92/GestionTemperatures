# Fonction pour verifier si acces internet ok
import urllib

def InternetOk():
    try :
        url = "https://www.google.com"
        urllib.urlopen(url)
        status = "Connected"
        #print("Toto : Connected")
        return True
    except :
        status = "Not connect"
        #print("Toto : Not Connected")
        return False
