#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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


from selenium import webdriver
import selenium

import win32gui
import re
import os
import zipfile



#personalisation des options(rep de download et adresse vers chromdriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "c:/tmp"}
options.add_experimental_option("prefs",prefs)
chromedriver = "c:/windows/system32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

driver.set_page_load_timeout(30)




class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""


def __init__(self):
    """Constructor"""
    self._handle = None


    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)


    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd


    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


#charge un fichier de paires pour un mois et une annee donnee
#renvoie le nom du fichier csv extrait
def loadpairemoisan(paire,mois,an):
    URL = "http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/"+paire+"/"+an+"/"+mois+"/"
    FileName = "HISTDATA_COM_NT_"+paire+"_T_BID_"+an+mois+".zip"
    RealFileName = "HISTDATA_COM_NT_"+pairename+"_T_BID"+an+mois+".zip"

    driver.get(URL)

    print("loaded")
#    toclic = None
#    while (toclic == None):
    toclic = driver.find_element_by_id("a_file")
            #.find_element_by_link_text(FileName) #le nom de fichier est l'objet clicable
    print("clic : ", FileName)
    print (toclic.text)

    #on attend la fermeture des popups qui serient apparues devant le bouton (message des cookies)
    canclick=0
    while canclick==0:
        try:
            toclic.click()
            canclick=1
        except selenium.common.exceptions.WebDriverException as e:
            z=e


    pathdownload = "c:/tmp/"+RealFileName #attention le nom est different entre le zip et le lien clic

    notfound = True
    while (notfound):
        if os.path.exists(pathdownload):
            notfound = False

    print("found")
    # on cherche dans le zip un fichier csv
    #on le decompress dans tmp
    #puis on enleve le zip
    zf = zipfile.ZipFile(pathdownload, 'r')

    for i in zf.filelist:
        if i.filename.find(".csv") != -1 :
            print("extract ",i.filename)
            newpath = zf.extract(i,path="c:/tmp")
            print(newpath)

    zf.close()
    os.remove(pathdownload)

    return newpath


#le main qui lit les fichiers sur le site, fabrique un zip et l'envoie dans le drive

#listemois=["01","02","03","04","05","06","07","08","09"]
listemois=["01"]
listepaires=["EURUSD","EURCHF","EURGBP"] #,"EURJPY","USDCAD","USDCHF","USDJPY","GBPCHF","GBPUSD","AUDUSD","EURCAD"]



print("identif OK")

for mois in listemois:

    # lecture des fichiers du mois sur le site
    listefic = []  # liste des fichier extraits
    for pairename in listepaires :
        print ("load")
        fichname = loadpairemoisan(pairename, mois, "2016")
        listefic.append(fichname)

    #on refusionne tout dans un zip du mois
    zipoutname = "BID"+mois+"2016"
    zfileout = zipfile.ZipFile("c:\\tmp\\"+zipoutname+".zip", 'w')
    for ficname in listefic:
        zfileout.write(ficname)

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
    filecsv = drive.CreateFile({"mimeType":"application/zip","title": zipoutname+".zip", "parents": [{"kind": "drive#fileLink", "id": fid}]})

    print("create ok")

    # ci dessous : le fichier part dans la racine du drive
    filecsv.SetContentFile("c:\\tmp\\"+zipoutname+".zip")

    print ("send "+zipoutname+" ok")