#!/usr/bin/env python
# -*- coding: utf-8 -*-



#readgogdrive : fichier contenant surtout des utilitaires de lecture des zip
# lit un mois sur le drive
#sauf si le zip BIDmmyy.zip est deja dans c\tmp : dans ce cas : lit le zip du tmp

# 30 oct 16 : ajout de generedata qui lit un paire dans ce zip

#27 dec 16 : je resuis ce fichier a la lecture dans google (ou sur tmp)
#il ne restera qu'un yield pour lire ligne par ligne un fichier sur le drive ou dans le tmp

#il fautdar faire un include depuis aileurs


#############################################
#strucutre des fichiers

# les fichiers sont lus a la base dans le site web
# un fichier zip est lu, avec dedans un fichier csv avec les ticks de une paire pour un mois
# la fonction clicselenium transfert ces donnees dans c:\tmp avec u fichier zip contenant toutes les paires pour 1 mois
#le fichier zip s'appelle bidMMYY
#les csv dedans ont juste le nom de la paire

#ces fichier zip des ticks de plusieurs paires pour 1 mois sont expedies a la main dans le drive

#readgoogle rappatrie un fichier zip (mois, annee) de googledrive dans c:\tmp
#getnomzip permet de calculer le nom d'une fichier tmp a partir de son mois, annee

#on peut creer un tableau de minutes pour tout un mois avec generedata
#le tableau contient numsample,date,begin

#on peut lire quelques jours d'un mois dans c:\tmp avec readlines(datedeb, nbjours, jour,nomzip,paire)
#qui yield nbjourslus,date,int(delta.total_seconds()/60),begin
# c a d : nombre de jours lus dans le fichier, date de la ligne, minute de la ligne depuis la date de debut, valeur bein
#cette fonction est utilisee pour lire une semaine de data, eventuellement dans 2 mois successifs

# c'est ce que fait readpaire : lecture d'une semaine dans une paire
#fait appel a readlines

#############################################

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

####### readgoogle #########################
# ----- lit un fichier defini par son annee et son mois dans le drive------
# gere les autorisations googledrive
# et l'enregistre dans c:\tmp
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
# #le nb minutes depuis debut du mois (1er du mois 0:00)
# la date
# la valeur de begin
def decodelinemois(laligne):
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
#positionné dans le repertoire temporaire (c:\tmp)
#import datetime
import time

def getnomzip(annee,mois): #annee est un string, week ens un nb
    stryear = str(annee)
    strmois=  str(mois).zfill(2)
    nomzip = r"c:\tmp\BID"+strmois+stryear+'.zip'  #nom du fichier zip correspondant
    return nomzip

################# generedata ####################
#fonction de lecture de fichier du drive ou temporaires
# par mois entiers
#lit une paire dans le zip nomzip
#et le met dans un tableau
def generedata(nomzip,paire):
    letab=[]
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    with z1.open(paire+".csv", mode='r') as read1:
        for laligne in read1 :
            numsample,date,begin = decodelinemois(laligne) # lecture de la ligne et calcule minute depuis debut du mois
            letab.append([float(numsample),begin])
    fh1.close()


    ###################  getlinemoispaire #####################
    # lit ligne par ligne dans le zip d'un mois pour une paire
    # ligne par ligne avec un yield
    # retourn None,None,None a la fin
    #retourne numeroechantillon (= nb min depuis debut mois), date, valeur de debut
    def getlinemoispaire(nomzip, paire):
        letab = []
        fh1 = open(nomzip, 'rb')
        z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
        with z1.open(paire + ".csv", mode='r') as read1:
            for laligne in read1:
                numsample, date, begin = decodelinemois(laligne)  # lecture de la ligne et nb mins depuis debut du mois
                yield numsample, date, begin
        fh1.close()
        return None,None,None

################### decodetime ###############################
#fonction decodant le temps datetime pour en faire un quadruplet
# jour heure minute jour de la semaine
# utile pour les graphs du mois
def decodetime(time):
    letuple = time.timetuple()

    day = letuple.tm_day()
    hour = letuple.tm_hour()
    minute = letuple.tmmin()
    weekday = letuple.wday()
    return day,hour,minute,weekday




# -----------------PAR ICI LE MAIN ----------------------------
import os.path

################## readlines ####################
# : lecture de qq jous dans un fichier mois
#lit nbjours dans un fichier csv contenant le mois pour une paire
# a partir du jour du mois =  jour
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
            numsample, date, begin = decodelinemois(laligne)  # lecture de la ligne

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



#pour test
if __name__ == '__main__':
    print("rien a faire")

    #lirepaire(2015,38,"EURUSD") NE PLUS UTILISER, cf readweekpaire.py

    #tab2 = generedata(nomfich, "USDCHF")

    #tabx1,tabyOpen1,tabyHigh1,tabyLow1,tabyClose1 = normalise2(tab1)
    #tabx2,tabyOpen2,tabyHigh2,tabyLow2,tabyClose2 = normalise2(tab2)

    #candlestick2_ohlc(tabx1, tabyOpen1,tabyHigh1,tabyLow1,tabyClose1)
    #candlestick2_ohlc(tabx2, tabyOpen2,tabyHigh2,tabyLow2,tabyClose2)

    #plt.show()

    #bin1min(tab1,tab2)

