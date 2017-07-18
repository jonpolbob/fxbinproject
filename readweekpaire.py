#!/usr/bin/env python
# -*- coding: utf-8 -*-


#fichier readweekpaire contient le necessaire pour lire une semaine d'une paire dans un fichier temporaire de c:\tmp
# paire

import readgogdrive
import clicseleniumsemaine

# ce fichier lit une semaine d'une paire dans un tablau
# et le met en candles

import datetime
import datesemaineutils

#lit tous les ticks d'une semaine de cette paire
#dans le tableau
#col 1 = minute depuis dimanche de la semaine, 17h00
#col2 : date-time
#col3 : valeur
def readweek(week,year,paire):
    tabout=[]
#calcul du mois de debut et de fain de la semaine
    deby,debm,debd = datesemaineutils.getdimanchefromweek(week,year)  # date debut de semaine
    datedeb = datetime.datetime(deby,debm,debd,hour=17) #demarre le dimanche a 17h
    finy, finm, find = datesemaineutils.getsamedifromweek(week,year)   # mois fin semaine
    print("lecture mois" , deby,debm,debd," jusqu'a", finy,finm)

    for laligne in readgogdrive.readlines(datedeb,6, debd, readgogdrive.getnomzip(deby,debm),paire):
           nbjourslus = laligne[0]
           # (laligne)
           #0 = nbjourslus
           #1 : datetime avec la date
           #2 = nb libutes depuis dimanche soir
           #3 valeur
           tabout.append([laligne[2],laligne[1],laligne[3]])

    #si il reste des jours a lire
    toread = 6-nbjourslus

    if toread != 0: #on lit les jours suivants a partir du 1er du mois
        datedeb2 =  datetime.datetime(finy,finm,1,hour=0) #demarre le 1 du mois suivant a 0h

        for laligne in readgogdrive.readlines(datedeb2,toread, 1, readgogdrive.getnomzip(finy,finm),paire):
                #print (laligne)
                # 0 = nbjourslus
                # 1 : datetime avec la date
                # 2 = nb libutes depuis dimanche soir
                # 3 valeur
                tabout.append([laligne[2], laligne[1], laligne[3]])

    return tabout

###################################################""
# utilistaire qui lit tous les ticks d'une semaine de cette paire
# et les range das un tableau
#les datas snt lues dans le csv de c:\tmp contannt tous les ticks du mois
# on a le nom de ce csv grace a loadpairmoisan de clicselenumsemaine
# qui renvoie un nom correct de .csv pour un mois/an/paire
# (eventuellement en chargeant ce fichier sur le web si il n'est pas la)

#dans le tableau de sortie
#col 1 = minute depuis dimanche de la semaine, 17h00
#col2 : date-time
#col3 : valeur
###################################################""
def readWeekInTmp(week,year,paire):
    tabout=[]

#calcul du mois de debut et de fain de la semaine
    deby,debm,debd = datesemaineutils.getdimanchefromweek(week,year)  # date debut de semaine
    datedeb = datetime.datetime(deby,debm,debd,hour=17) #demarre le dimanche a 17h
    finy, finm, find = datesemaineutils.getsamedifromweek(week,year)   # mois fin semaine
    print("lecture mois" , deby,debm,debd," jusqu'a", finy,finm)

    strdeby = str(deby)  #conversion en string bien formatee
    strdebm = str(debm)  # conversion en string bien formatee

    nomzipdebut = clicseleniumsemaine.loadpairemoisan(paire,strdeby,strdebm)


    for laligne in readgogdrive.readlines(datedeb,6, debd, readgogdrive.getnomzip(deby,debm),paire):
           nbjourslus = laligne[0]
           # (laligne)
           #0 = nbjourslus
           #1 : datetime avec la date
           #2 = nb libutes depuis dimanche soir
           #3 valeur
           tabout.append([laligne[2],laligne[1],laligne[3]])

    #si il reste des jours a lire
    toread = 6-nbjourslus

    if toread != 0: #on lit les jours suivants a partir du 1er du mois
        datedeb2 =  datetime.datetime(finy,finm,1,hour=0) #demarre le 1 du mois suivant a 0h

        for laligne in readgogdrive.readlines(datedeb2,toread, 1, readgogdrive.getnomzip(finy,finm),paire):
                #print (laligne)
                # 0 = nbjourslus
                # 1 : datetime avec la date
                # 2 = nb libutes depuis dimanche soir
                # 3 valeur
                tabout.append([laligne[2], laligne[1], laligne[3]])

    return tabout




#renvoie un tableau de candles a la place d'un tableau de ticks
# au format candlestick_ohlc

def candelize(tableau):
    tabout=[]
    valeur = tableau[0][2]
    valopen = valeur #valeur
    valclose = valeur  # valeur
    vallo = valeur  # valeur
    valhi = valeur  # valeur
    nbmesures=0

    curidx = tableau[0][0]  # numero premiere minute du tableau
    lstidx = curidx
    for line in tableau:
        curidx = line[0]
        valeur = line[2]
        if curidx != lstidx:  #changement de minute
          #  print([lstidx, valopen, valhi, vallo, valclose])
            tabout.append([lstidx,nbmesures,valopen,valhi,vallo,valclose]) #ds tableau sortie
            valopen = valeur  # valeur entree
            vallo = valeur # valeur mini
            valhi = valeur # valeur max
            nbmesures =0
            print (line[1]) #on ecrit la date

        nbmesures = nbmesures+1
        lstidx = curidx
        if valeur > valhi:
            valhi = valeur
        if valeur < vallo:
            vallo = valeur
        valclose = valeur  #valeur sortie

    return tabout

if __name__ == '__main__' :

    letableau = readweek(5,2016,'AUDUSD')
    tabcandle = candelize(letableau)
    print (tabcandle)






