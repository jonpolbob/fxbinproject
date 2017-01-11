#!/usr/bin/env python
# -*- coding: utf-8 -*-

#utilistaires de normalisation des donnees des tableaux de valeurs

#fonction de normalisation
#normalisation premier mode : on prend les 50 dernieres valeurs et on en fait la moyenne -> ce sera la moyenne
#on ne noermalise par l'ecart type
#recoit un tableau en entree

def normalise2(tabin):
    localstackX=[]
    localstackY = []
    outtabX=[]
    outtabY = []
    lasttime = 0
    ledeb = None
    outtabYdeb = []
    outtabYfin = []
    outtabYmin = []
    outtabYmax = []

    for laline in tabin:
        if ledeb == None: #premiere ligne = on int la candle
            ledeb = laline[1]
            lemin = laline[1]
            lemax = laline[1]
            lasttime = laline[0]

        if laline[0] == lasttime: #meme heure on met a jour les vleurs de la candle
            lemax = max(lemax,laline[1])
            lemin = min(lemax,laline[1])
            lafin = laline[1]
        else : #changement d'heure : on normalise le candle et on genere la sortie
            #on empile la nouvelle valeur pour le calcul des moyennes
            lamediane = (ledeb + lafin)/2
            if len(localstackY) > 30: #il y a assez de valeurs
                moyenne = sum(localstackY) / len(localstackY)  # le stack avant la candle
                # localstackX.remove(localstack[0])
                localstackY.remove(localstackY[0])

            # localstackX.append(laline[0])
            localstackY.append(lamediane) #la pile est pleine de medianes

            #on enregistre la candle
            if len(localstackY) > 30:  # il y a assez de valeurs : on fait une candle normalisee
                outtabX.append(laline[0])
                outtabYdeb.append(ledeb  - lamediane)
                outtabYfin.append(lafin - lamediane)
                outtabYmax.append(lemax - lamediane)
                outtabYmin.append(lemin - lamediane)

            #on init la prochaine candle
            ledeb = laline[1]
            lemin = laline[1]
            lemax = laline[1]
            lafin = laline[1]
            lasttime = laline[0]

    return outtabX, outtabYdeb, outtabYmax, outtabYmin, outtabYfin

