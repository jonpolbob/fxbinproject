#!/usr/bin/env python
# -*- coding: utf-8 -*-

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



def generedata(nomzip,paire):
    fh1 = open(nomzip, 'rb')
    z1 = zipfile.ZipFile(fh1)  # classe lisant le zipdanzs le fichier ouvert
    with z1.open(paire+".csv", mode='r') as read1:
        for laligne in read1 :
            date,begin = decodeline(laligne)
            print (date)

    fh1.close()

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
generedata(nomfich, "EURUSD")



