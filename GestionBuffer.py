TableauBuffer = [] # Creation du tableau qui sert de buffer si internert est off

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
