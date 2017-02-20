import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

fifo=[]

#clcule les fatures sur les donnees de la fifo
#on fait les calculs sur les 20 elements de la fifo
#la fifo doit etre inversee c a d le 0 est la derniere valeur avant l'evenement
def calculfeatures(revfifo):
    #premiere feature  : on regarde
    todraw = []
    for value in revfifo:
        todraw.append(value[1:])

    #plt.plot()
    #plt.show()

# ici il reste a generer le tableau des features
# les arguments du tableau des features sont pour l'instant les bandes et les boliing
# il faut generer un tableau avec features positives et features negatives
def generefeatures(marksX, tabcandle, upband, dnband):
    global fifo
    for values in zip(tabcandle,upband,dnband):
        #on met tout dans une seule liste
        candle = values[0]
        candle.append(values[1])
        candle.append(values[2])

        print(candle)
        fifo.append(candle)
        #print (fifo

        if len(fifo)>20:
            fifo.pop(0) #on vire le plus ancien

        print(len(fifo))
        #ici n a une fifo avec les valeurs
        #et marksx qui contient les index des evenements detectes
        #on calcule les features de tout le monde, ce qui est un event on le range dans les events, ce qui ne l'est pas on le range de laures cote


        revfifo = list(reversed(fifo))  #liste contenant a fifo inversee (0 = derniere valeur avant evenement)
        featureslist = calculfeatures(revfifo)


