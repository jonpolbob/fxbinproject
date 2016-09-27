#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

from selenium import webdriver
import win32gui
import re
import os
import zipfile

#personalisation des options(rep de download et adresse vers chromdriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "c:/tmp"}
options.add_experimental_option("prefs",prefs)
chromedriver = "c:/windows/system32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, tions=options)

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

    toclic = driver.find_element_by_link_text(FileName) #le nom de fichier est l'objet clicable
    toclic.click()

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
    print (zf.filelist)
    for i in zf.filelist:
        if i.filename.find(".csv") != -1 :
            print("extract ",i.filename)
            newpath = zf.extract(i,path="c:/tmp")
            print(newpath)

    zf.close()
    os.remove(pathdownload)

    return newpath


#listemois=["01","02","03","04","05","06","07","08","09"]
listemois=["01"]
listepaires=["EURUSD","EURCHF","EURGBP"] #,"EURJPY","USDCAD","USDCHF","USDJPY","GBPCHF","GBPUSD","AUDUSD","EURCAD"]

for mois in listemois:

    listefic = []  # liste des fichier extraits
    for pairename in listepaires :
        fichname = loadpairemoisan(pairename, mois, "2016")
        listefic.append(fichname)

    #on refusionne tout dans un zip du mois
    zipoutname = "BID"+mois+"2016"
    zfileout = zipfile.ZipFile(zipoutname+".zip", 'w')
    for ficname in listefic:
        zfileout.write(ficname)



