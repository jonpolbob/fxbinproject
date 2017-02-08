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
#sort une de 0 avec un 1 sur les points interessants
#super bourrin pour que ca marche
#pdtable est une table panda a 1 colonne

def detectinteressant(pdtable,ypos): #calcul de bolinger
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

            valeurdeb = lafifo[0][1][0] #ohlc : on prend le open
            idxdeb = lafifo[0][0] #index de la mesure

            lafifo.pop(0) #on vire la valueur de reference, on travaille sur le reste de la pile

            Found =True
            #test aucune descente (low en dessous du begin)
            for i in lafifo:
                if (valeurdeb > i[1][2]) : #il faut pas que un low de l'ensemble soit < ouverture
                    Found=False
                    break

            #on n'a aucun point dans la fifo plus petit que la valeur
            #donc c'est ok
            if Found: #on affichera une marque devant le debut
                resuX.append(idxdeb)
                resuY.append(ypos[idxdeb]) #position = upperband passee en argumlent

    return resuX,resuY






