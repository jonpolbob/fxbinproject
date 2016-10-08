#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

#meme programme que save and save mais appelle clicselenium au lieu de tout reecrire


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

import clicselenium  #pour le import

#penser a couper skype !
#sinon port 8080 est bloqué
#en mode cmd adminstrateur
#net stat -a -n -o |findstr 8080
# lire le pid de la tache puis
#taskkill /F /pid 1234

#demarrage des autorisations google a placer avant demarrage de selenium ?
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


#le main qui lit les fichiers sur le site, fabrique un zip et l'envoie dans le drive

listemois=["01","02","03","04","05","06","07","08","09"]
listepaires=["EURUSD","EURCHF","EURGBP","EURJPY","USDCAD","USDCHF","USDJPY","GBPCHF","GBPUSD","AUDUSD","EURCAD"]

print("identif OK")

for mois in listemois:

    # lecture des fichiers du mois sur le site
    # et on en fait un zip
    zipfichname = clicselenium.liremois(mois,listepaires)
    print("nom du fichier zip :",zipfichname)
    shortname =  os.path.relpath(zipfichname,"c:\\tmp")


    #on transfert le zip dans le drive
    fid = ""

    #on cherche le ID du dossier 'data' diu drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        if file1['title'] == 'data':
            fid = file1['id']
            print("found : ", fid)

    #on envoie le fichier zip dans ce dossier
    # les bon arguments pour indiquer le id d'un sous repertoire ou ecrire
    # et changer le titre dans le drive
    filecsv = drive.CreateFile({"mimeType":"application/zip","title": shortname , "parents": [{"kind": "drive#fileLink", "id": fid}]})

    print("create ok")

    # ci dessous : le fichier part dans la racine du drive
    filecsv.SetContentFile(zipfichname)
    filecsv.Upload()

    print ("send "+zipfichname+"dans"+shortname+ " ok")