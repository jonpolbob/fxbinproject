#!/usr/bin/env python
# -*- coding: utf-8 -*-


import readweekpaire
import calculsframe
import generefeatures

import numpy as np
import pandas as pd
from matplotlib.finance import  candlestick_ohlc
import matplotlib.pyplot as plt
#34 2015 = 17 aout
#36 2015 : aout sept
#40 pour 10 2015
import matplotlib

print("version matplotlib ",matplotlib.__version__)

eventstab = []

annee = 2016
paire = 'EURUSD'
semainedeb = 24
semainefin = 45
debut = 0000
fin = 7000

for semaine in range(semainedeb,semainefin):
    generefeatures.clearfifo()

    grandtableau = readweekpaire.readweek(semaine, annee, paire)
    letableau = grandtableau[debut:fin]

    lasize = len(letableau)

    tabcandle = readweekpaire.candelize(letableau)
    print("---------------------------")
    for z in tabcandle:
        print (z)
    print("---------------------------")

    print ("lu : ", len(tabcandle),"lignes")

#remplissage d'une table avec NaN dans les cases sans resultat
#et on envoie ca dans un panda dataframe pour les calculs statistiques
    nantable = np.zeros([lasize,4])  #sous table
    nantable[:]=np.nan   #init a nan

    mini = lasize
    maxi =0

#on cree une table avec juste les open et l'index

    for i in tabcandle: #remplissage des cases avec une donnee
        nantable[i[0]][0:4] = i[1:5] #4 valeurs de i utilisees : on utilise le open
#       print(i[1])
        mini =  min(i[0],mini)
        maxi = max(i[0], maxi)

    pdtable = pd.DataFrame(nantable[mini:maxi][:]) #on limite aux cases remplies

#ici on retravaille sur le panda ame ur faire les moyennes mobiles, etc etc
#tableau avec un index pour l'axe des x
    index = np.arange(mini,maxi) #index en accord avec les cases remplies

#utilisation des valeurs de la table
    upband,dnband,upband80,dnband80 = calculsframe.calcbolingerreduced(pdtable,[20,2.4,0.8])  #params = avg, hi bol , low bol
    mm80 = calculsframe.calcmm80(pdtable)

    upbandarray = np.array(upband)
#2eme arg = position Y ou mettre la marque
    #nouveau detectinteressant : utilise les courbes bollinger et average80
    marksX, marksY, marksZ, count= calculsframe.detectinteressant(pdtable,[upband,dnband,upband80,dnband80,mm80]) #2eme col = high

    #marksY=upband[marksX] #liste des valeurs dont l'index est dans markx
    print('resultats ',count)

    #ono calcule le resultat de ce marquage
    calculsframe.calcresu(pdtable, marksX, marksY, [upband,dnband,upband80,dnband80,mm80])


    # Plot two charts to assess trades and equity curve
    fig = plt.figure()
    fig.patch.set_facecolor('white')  # Set the outer colour to white
    ax1 = fig.add_subplot(211, ylabel='Price in $')

#plot les marks
    marker_style = dict(color='red', marker='v',
                    markersize=8, linestyle='None', markerfacecoloralt='gray')

    marker_styleZ = dict(color='blue', marker='o',
                        markersize=8, linestyle='None', markerfacecoloralt='gray')

    marker_style2 = dict(color='red', marker='o',
                    markersize=4, linestyle='None', markerfacecoloralt='gray')


#marks est en index du tableau il faut lui ajouter debut
    marksXpos = np.array(marksX)+mini
# Plot the "buy" trades against
#ax1.plot(upband,'^', markersize=10, color)
#ax1.plot(upbale1nd,'^', markersize=10, color='m'
    candlestick_ohlc(ax1, tabcandle, width=.8,colorup='#53c156', colordown='#ff1717')
    ax1.plot(index,upband,'^', ls='-', markersize=1, color='m')
    ax1.plot(index,dnband,'^', ls='-', markersize=1, color='g')
    ax1.plot(index, upband80, '^', ls='-', markersize=1, color='m')
    ax1.plot(index, dnband80, '^', ls='-', markersize=1, color='g')
    ax1.plot(index, mm80, '^', ls='-', markersize=1, color='b')

    #ax1.plot(marksXpos,upband[marksX],**marker_style)
    ax1.plot(marksXpos, marksY, **marker_style)
    ax1.plot(marksXpos, marksZ, **marker_styleZ)
    #markx2 = marksX-10
    markx2 = list(map(lambda x: x - 10, marksX))   #-10 pour chaque irem ax1.plot(markx2,upband[marksX],**marker_style2)
    plt.show()

    #ici il faut enregistrer les valeurs utilisees autour de tous ces index
    #on passe par un tableau eventstab dans lequel on va enregistrer les parametres de tout ce qui est marque, 10 candle avant
    ## et 10 candle apres
#    eventstab = generefeatures.extracteventsdata(semaine, eventstab, marksX, tabcandle, upband, dnband)
    #featurestab = generefeatures.generefeatures(semaine,featurestab,marksX,tabcandle,upband,dnband)


eventstab=[]
#eventstab contient semaine, idx, [[candle-i],up-i,dn-i],[[candle-(i-1)],up-i,dn-(i-1)]
#pour avoir les candle : il faut un tableau ligne[2:22][0]

for ligne in eventstab :
    print(ligne)
    fig = plt.figure()
    fig.patch.set_facecolor('white')  # Set the outer colour to white
    ax1 = fig.add_subplot(211, ylabel='Price in $')

    tabdata = np.array(ligne[2:22]) #tableau des 20 datas

    petitcandle = []
    toto = tabdata[:,0]

    for idx,candle in zip(range(-10,10),toto): #contient un index + les candles de -10 a 10
        truc=candle[1:]
        eut = [idx]
        eut.extend(truc)
        petitcandle.append(eut) #liste concatenant l'index et les candles
    candlestick_ohlc(ax1, petitcandle, width=.8, colorup='#53c156', colordown='#ff1717')
    #ax1.plot(index, upband[], '^', ls='-', markersize=1, color='m')
    #ax1.plot(index, dnband, '^', ls='-', markersize=1, color='g')
    #ax1.plot(marksXpos, upband[marksX], **marker_style)
    plt.show()

