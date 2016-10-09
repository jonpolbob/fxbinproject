#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

#recupere une paire du google drive


def readgoogle(paire,annee,mois):
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
    print (drive.ListFile(datalistfiles).GetList())

    for file1 in datalistfiles:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['title'] == zipfichname:
            fileid = file1['id']
            print("found : ", fileid)

#maintenant il faut trouver le ID du fichier


    #on cree un fichier comme pour l'enregistrement
    filezip = drive.CreateFile({"mimeType": "application/zip", "id":fileid, "parents": [{"kind": "drive#fileLink", "id": dataid}]})
    filezip.GetContentFile("toto") #pour test : on rajoute un _ avcant le nom



readgoogle("EURUSD","2015","10")
