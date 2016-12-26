#!/usr/bin/env python
# -*- coding: utf-8 -*-

#readgogdrive : lit un mois sur le drive
#sauf si le zip BIDmmyy.zip est deja dans c\tmp : dans ce cas : lit le zip du tmp

# 30 oct 16 : ajout de generedata qui lit un paire dans ce zip

#27 dec 16 : je resuis ce fichier a la lecture dans google (ou sur tmp)
#il ne restera qu'un yield pour lire ligne par ligne un fichier sur le drive ou dans le tmp

#il fautdar faire un include depuis aileurs

__author__ = 'cagibi'

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import zipfile
import datetime
#recupere une paire du google drive
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc

# ----- lit un fichier dans le drive------

def readgoogle(annee,mois):
    # demarrage des autorisations google a placer avant demarrage de selenium ?
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    zipfichname="BID"+mois+annee+".zip" #nom sur le drive
    print("cherche ",zipfichname)

    #on cherche le id du dossier data
    # on transfert le zip dans le drive
    dataid = ""

    # on cherche le ID du dossier 'data' diu drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['title'] == 'data':
            dataid = file1['id']
            print("found : ", dataid)

            # on envoie le fichier zip dans ce dossier
            # les bon arguments pour indiquer le id d'un sous repertoire ou ecrire
            # et changer le titre dans le drive
    print("scan dir ok");

    #lecture des fichiers de data
    #la query cherche le dossier dataid dans parents
    datalistfiles = {'q': "'{}' in parents and trashed=false".format(dataid)}
    print(datalistfiles)
    drivefile = drive.ListFile(datalistfiles).GetList()
    print (drivefile)

    for file1 in drivefile:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['title'] == zipfichname:
            fileid = file1['id']
            print("found : ", fileid)

#maintenant il faut trouver le ID du fichier


    #on cree un fichier comme pour l'enregistrement
    #filezip = drive.CreateFile({"mimeType": "application/zip", "id":fileid, "parents": [{"kind": "drive#fileLink", "id": dataid}]})
    filezip = drive.CreateFile({"mimeType": "application/zip", "id": fileid})
    namzipdisk = "c:\\tmp\\" + zipfichname
    filezip.GetContentFile(namzipdisk) #pour test : on rajoute un _ avcant le nom
    return namzipdisk

# ---------- decode une ligne de fichier csv ------------------
# renvoie
# #le nb minutes depuis debut du mois
# la date
# la valeur de begin
def decodeline(laligne):
    colonnes = laligne.split(b';')
    # print (colonnes)
    ladate = colonnes[0]
    annee = int(ladate[0:4])
    mois = int(ladate[4:6])
    jour = int(ladate[6:8])
    heure = int(ladate[9:11])
    minute = int(ladate[11:13])
    secondes = int(ladate[13:15])
    datenumber = datetime.datetime(year=annee, month=mois, day=jour, hour=heure, minute=minute, second=secondes)
    datenumberdebut = datetime.datetime(year=annee, month=mois, day=1, hour=0, minute=0, second=0)
    deltatime = datenumber - datenumberdebut
    deltamins = int(deltatime.total_seconds()/60)

    beginvalue = colonnes[1]

   #deltamins = nb minutes depuis debut du mois
   #datenumber = la date-heure de cette mesure
    return deltamins, datenumber, float(beginvalue)


#renvoie le nom de 1 ou 2 zip correspondant a cette semaine
#import datetime
import time

def getnomzip(annee,mois): #annee est un string, week ens un nb
    stryear = str(annee)
    strmois=  str(mois).zfill(2)
    nomzip = r"c:\tmp\BID"+strmois+stryear+'.zip'  #nom du fichier zip correspondant
    return nomzip



#generedata
#lit un paire dans le zip
#et le met dans un tableau
def generedata(nomzip,paire):
    letab=[]
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    with z1.open(paire+".csv", mode='r') as read1:
        for laligne in read1 :
            numsample,date,begin = decodeline(laligne) # lecture de la ligne
            letab.append([float(numsample),begin])
    fh1.close()

    # generedata
    # le zip ligne par ligne avec un yield
    # retourn None,None,None a la fin
    def getlinemoispaire(nomzip, paire):
        letab = []
        fh1 = open(nomzip, 'rb')
        z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
        with z1.open(paire + ".csv", mode='r') as read1:
            for laligne in read1:
                numsample, date, begin = decodeline(laligne)  # lecture de la ligne
                yield numsample, date, begin
        fh1.close()
        return None,None,None


#fonction decodant le temps datetime pour en faire un temps jour heure minute jour de la semaine utile pour les graphs du mois
def decodetime(time):
    letuple = time.timetuple()

    day = letuple.tm_day()
    hour = letuple.tm_hour()
    minute = letuple.tmmin()
    weekday = letuple.wday()
    return day,hour,minute,weekday



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


# -----------------PAR ICI LE MAIN ----------------------------
import os.path


#lit nbjours du nom de fichier a partir du jour du mois =  jour
#ligne par ligne
#renvoie le nb de minutes entre la ligne et datedeb
#yield la date et la valeur
#renvoie le nb de jours lus quand le balayage est fini (None, nbjourslus)
#charge dans le tableau le nombre de jourd nbjours a partir du jour jour
def readlines(datedeb, nbjours, jour,nomzip,paire):
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    nbjourslus=0
    lstday = -1
    with z1.open(paire + ".csv", mode='r') as read1:
        for laligne in read1:
            numsample, date, begin = decodeline(laligne)  # lecture de la ligne

            if lstday != date.day: #la date a changé
                if nbjourslus != 0 :  #on a commence a lire des jours
                    nbjourslus = nbjourslus + 1  # un nouveau jour
                else:
                    print("jour",date.day)  #on n'a pas commence a lire des jours : on saute

            lstday = date.day

            if date.day == jour: #on a atteint le jour recherche
                nbjourslus = 1 #on commence

            if nbjourslus > nbjours : #on a lu le bon nombre de jours
                break #fin du for


            if nbjourslus !=0 :
                delta = date - datedeb  # delta depuis debut semaine
                yield nbjourslus,date,int(delta.total_seconds()/60),begin  #date, valeur debut

    fh1.close()





#lit une paire pour une semaine de l'annee

def lirepaire(annee, semaine,paire):
    #calcul des mois et annee a utiliser (une semaine peut etre a cheval sur 2 mois)
    jourdeb, moisdeb, anneedeb, jourfin, moisfin, anneefin = getnomzip(annee,semaine)  # annee est un string, week ens un nb

    #lecture du mois ou ca commence
    #regarde si le fichier existe
    mois = "00" + int(moisdeb)
    zipfichname = "BID" + mois + str(anneedeb) + ".zip"  # nom sur le drive
    namzipdisk = "c:\\tmp\\" + zipfichname
    if os.path.isfile(namzipdisk):
        print("fichier "+namzipdisk+" retrouve")
        nomfich = namzipdisk
    else:
        print("lecture fichier " + namzipdisk + " sur le drive")
        nomfich = readgoogle(str(anneedeb),mois[:-2])

    tableau=[]
    nbjours=5

    #on lit ce fichier dans le tableau (ca l'imprime a l'ecran)
    tableau,nbjourslus = loadtableau(tableau, nbjours, jour,nomfich, paire)  #charge le tableau avec les premiers jours

    #il y a un deuxieme mois a lire pour cette semaine
    if moisfin != moisdeb:  #a cheval sur 2 mois
        mois = "00" + int(moisfin)
        zipfichname = "BID" + mois + str(anneefin) + ".zip"  # nom sur le drive
        namzipdisk = "c:\\tmp\\" + zipfichname
        if os.path.isfile(namzipdisk):
            print("fichier " + namzipdisk + " retrouve")
            nomfich = namzipdisk
        else:
            print("lecture fichier " + namzipdisk + " sur le drive")
            nomfich = readgoogle(str(anneefin), mois[:-2])

        #on lit le nouveau mois a partir du 1
        tableau,nbjourslus = loadtableau(tableau, 5-nbjourslus, 1,nomfich, paire)  #charge le tableau avec les premiers jours

    print(tableau)


#pour test
if __name__ == '__main__':

    lirepaire(2015,38,"EURUSD")

    #tab2 = generedata(nomfich, "USDCHF")

    #tabx1,tabyOpen1,tabyHigh1,tabyLow1,tabyClose1 = normalise2(tab1)
    #tabx2,tabyOpen2,tabyHigh2,tabyLow2,tabyClose2 = normalise2(tab2)

    #candlestick2_ohlc(tabx1, tabyOpen1,tabyHigh1,tabyLow1,tabyClose1)
    #candlestick2_ohlc(tabx2, tabyOpen2,tabyHigh2,tabyLow2,tabyClose2)

    plt.show()

    #bin1min(tab1,tab2)

