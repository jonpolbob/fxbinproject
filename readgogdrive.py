#!/usr/bin/env python
# -*- coding: utf-8 -*-

#readgogdrive : lit un mois sur le drive
#sauf si le zip BIDmmyy.zip est deja dans c\tmp : dans ce cas : lit le zip du tmp

# 30 oct 16 : ajout de generedata qui lit un paire dans ce zip



__author__ = 'cagibi'

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import zipfile
import datetime
#recupere une paire du google drive


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

#decode une ligne de fichier csv
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
    beginvalue = colonnes[1]
    # print(ladate)
    # print (annee,mois,jour,heure,minute)
    # print(datenumber.year, datenumber.month, datenumber.day,datenumber.hour, datenumber.minute)
    # print (float(begin))
    return datenumber, float(beginvalue)

#generedata
#lit un paire dans le zip
#et le met dans un tableau
def generedata(nomzip,paire):
    letab=[]
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    with z1.open(paire+".csv", mode='r') as read1:
        for laligne in read1 :
            date,begin = decodeline(laligne)
            letab.append([date,begin])
            print (date)
    fh1.close()
    return letab


def decodetime(time):
    letuple = time.timetuple()

    day = letuple.tm_day()
    hour = letuple.tm_hour()
    minute = letuple.tmmin()
    weekday = letuple.wday()
    return day,hour,minute,weekday


#bin1Min fait un fichier bin 1 minute avec les 2 tableaux en entree
def bin1min(year,month,tab1,tab2):
    currentday=1
    currenthour=0
    currentmin=0
    currenttime = (currentday*24+currenthour)*60+currentmin
    currentdatime = datetime.datetime(year=year,month=month,day=currentday)
    currentdayw = currentdatime.timetuple().tm_wday

    time1finish = False
    time2finish = False

    item1 = tab1.__iter__()
    item2 = tab2.__iter__()
    #on commence par un debut de tranche de temps
    newtime = True; #on est a un debut de tdt
    hasvalue1 = False #pas encore de valeur pour le 2
    hasvalue2 = False #pas encore de valeur pour le 1
    candle1 = []

    deb1=-1
    max1=-1
    min1=-1
    fin1 = -1

    while (True):

        if hasvalue1 == False:
            deb1 = item1[valeur]
            fin1 = item1[valeur]
            max1 = item1[valeur]
            min1 = item1[valeur]
            hasvalue1 = True

        fin1 = item1[valeur]

        if max1 < item1[valeur]:
            max1 = item1[valeur]
        if min1 > item[valeur]:
            min1 = item[valeur]

        if hasvalue1 == False:
           deb2 = item2[valeur]
           fin2 = item2[valeur]
           max2 = item2[valeur]
           min2 = item2[valeur]
           hasvalue2 = True

        fin2 = item2[valeur]
        if max2 < item2[valeur]:
           max2 = item2[valeur]
        if min2 > item[valeur]:
          min2 = item[valeur]

        day, hour, minute, weekday = decodetime(item1)
        if ((day*24+hour)*60+min) > currenttime :  #le temps 1 a depasse le temps courant
            time1finish=True;

        day, hour, minute, weekday = decodetime(item2)
        if ((day * 24 + hour) * 60 + min) > currenttime: #le temps 2 a depasse le temps courant
            time2finish = True;

        #ici on a fini une tranche de temps (qui a ete remplie ou non)
        if time1finish and time2finish : # timebin finie
            if hasvalue1: #il y a des valeurs pour 1
                candle1.append([currenttime,currentdayw,day,hour,minute,deb1,max1,min1,fin1])

            #on passe au temps suivant
            currentday = 1
            curenthour = 0
            currentmin = currentmin+1

            if currentmin == 60:
                currentmin =0
                currenthour = currenthour+1
                if currenthour == 24 :
                    currenthour =0
                    currentday = currentday+1
            currenttime = (currentday * 24 + currenthour) * 60 + currentmin

            newtime=True


        if not time2finish:
            item2 = tab2.__next__()

        if not time1finish:
            item1 = tab1.__next__()


    return




import os.path

#on test si on a deja charge de le zip
annee = "2015"
mois = "10"

#regarde si le fichier existe
zipfichname = "BID" + mois + annee + ".zip"  # nom sur le drive
namzipdisk = "c:\\tmp\\" + zipfichname
if os.path.isfile(namzipdisk):
    print("fichier "+namzipdisk+" retrouve")
    nomfich = namzipdisk
else:
    print("lecture fichier " + namzipdisk + " sur le drive")
    nomfich = readgoogle("2015","10")

#on traite ce fichier (ca l'imprime a l'ecran)
tab1 = generedata(nomfich, "EURUSD")
tab2 = generedata(nomfich, "USDCHF")

bin1min(tab1,tab2)

