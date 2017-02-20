import pandas as pd
import numpy as np

# toutes sortes de calculs sur le dataframe

def calcbolinger(pdtable,index):#calcul de bolinger
    length=30
    numsd=2.0

    ave = pdtable[2].rolling(center=True,window=30).mean()
    #sd = pd.stats.moments.rolling_std(pdtable,length)
    sd = pdtable[2].rolling(center=True,window=30).std()
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)

    return upband,dnband




#detecte une zone interessante dans un dataframe de candle
#sort une liste des index qui marchent
#super bourrin pour que ca marche
#pdtable est une table panda a 1 colonne
#la liste en sortie contient l'indice de la premiere candle de la zone detectee

def checkfifo(lafifo):
    valeurdeb = lafifo[0][1][0]  # ohlc : on prend le open
    idxdeb = lafifo[0][0]  # index de la mesure

    Found = True
    # test aucune descente (low en dessous du begin)
    for i in lafifo:
        if (valeurdeb > i[1][2]):  # il faut pas que un low de l'ensemble soit < ouverture
            Found = False
            break
  # on n'a aucun point dans la fifo plus petit que la valeur
    # donc c'est ok
    # n ne detecte rien qui ne soit pas paeres 10 valeurs
    # il faut un peu de donnees dans le passe (par ex 10) pour pouvoir detecter un evenent


    return Found and idxdeb > 10,


#fait la liste des points interessants
# on sort un tableau contenant les index des points interessants
def detectinteressant(pdtable): #calcul de bolinger
    lafifo =[]
    resuX=[]
    resuY = []

    #pour iterer sur les lignes de pandas il faut faire iterrows.
# on dirait que  un simle iteratuer renvoie des scalaires
    for idx,lacandle in pdtable.iterrows():

        linelist = lacandle.values.tolist()

        #on cree la fifo
        lafifo.append([idx,linelist])

        if (len(lafifo) > 10):

            found,ix = checkfifo(lafifo)

            lafifo.pop(0) #on vire la valueur de reference, on travaille sur le reste de la pile

            if found : #on affichera une marque devant le debut
                resuX.append(ix)

    return resuX

