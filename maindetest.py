#!/usr/bin/env python
# -*- coding: utf-8 -*-


import readweekpaire
import calculsframe

import numpy as np
import pandas as pd
from matplotlib.finance import  candlestick_ohlc
import matplotlib.pyplot as plt
#34 2015 = 17 aout
#36 2015 : aout sept
import matplotlib

print(matplotlib.__version__)

letableau = readweekpaire.readweek(32, 2015, 'AUDUSD')
tabcandle = readweekpaire.candelize(letableau)
print("---------------------------")
for z in tabcandle:
    print (z)
print("---------------------------")

print ("lu : ", len(tabcandle),"lignes")

#remplissage d'une table avec NaN dans les cases sans resultat
#et on envoie ca dans un panda dataframe pour les calculs statistiques
nantable = np.zeros([7200,4])  #sous table
nantable[:]=np.nan   #init a nan

mini = 7200
maxi =0

#on cree une table avec juste les open et l'index

for i in tabcandle: #remplissage des cases avec une donnee
   nantable[i[0]][0:4] = i[1:5] #4 valeurs de i utilisees : on utilise le open
#   print(i[1])
   mini =  min(i[0],mini)
   maxi = max(i[0], maxi)

pdtable = pd.DataFrame(nantable[mini:maxi][:]) #on limite aux cases remplies

#ici on retravaille sur le panda Dataframe pour faire les moyennes mobiles, etc etc
#tableau avec un index pour l'axe des x
index = np.arange(0,(maxi-mini)) #index en accord avec les cases remplies

#utilisation des valeurs de la table
upband,dnband = calculsframe.calcbolinger(pdtable,index)

upbandarray = np.array(upband)
#2eme arg = position Y ou mettre la marque
marksX= calculsframe.detectinteressant(pdtable) #2eme col = high
#marksY=upband[marksX] #liste des valeurs dont l'index est dans markx


# Plot two charts to assess trades and equity curve
fig = plt.figure()
fig.patch.set_facecolor('white')  # Set the outer colour to white
ax1 = fig.add_subplot(211, ylabel='Price in $')

#plot les marks
marker_style = dict(color='cornflowerblue', marker='v',
                    markersize=4, linestyle='None', markerfacecoloralt='gray')




# Plot the "buy" trades against
#ax1.plot(upband,'^', markersize=10, color)
#ax1.plot(upband,'^', markersize=10, color='m'
candlestick_ohlc(ax1, tabcandle, width=.8,colorup='#53c156', colordown='#ff1717')
ax1.plot(index,upband,'^', ls='-', markersize=1, color='m')
ax1.plot(index,dnband,'^', ls='-', markersize=1, color='g')
ax1.plot(marksX,upband[marksX],**marker_style)
plt.show()



#ici il reste a generer le tbaleau des features
#les arguments du tableau des features sont pour l'instant les bandes et les boliing
#il faut generer un tableau avec features positives et features negatives
def generefeatures(marksX,tabcandle,upband,dnband):
    


featurestab = generefeatures(marksX,tabcandle,upband,dnband)





