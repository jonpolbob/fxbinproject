#!/usr/bin/env python
# -*- coding: utf-8 -*-

#programme lisant les datas sur free-forex, lit les paires d'un mois annee en bid ou call
#les dezippe , met ensemble toutes les paires d"un meme mois an
#et en fait un zip

#il reste juste a tout experdier dans googledrive

#penser a mettre chromedriver.exe dans le path

#selon les parametres de chrome il y a ou non un message d'alerte des cookies
# avec firefow ca y est, avec chrome ca n'y est pas toujours

#corection le 30 dec 1- : les exceptions de selenium ont changé par rapport au source d'origine (python 3 ?)
#rajput de l'effacement des csv a la fin de la fabrication du zip pour eviter d'inclure dans le zip d'un autre mois les csv d'un mois precedent pas recupere


__author__ = 'cagibi'

from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile

# personalisation des options(rep de download et adresse vers chromdriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "c:/tmp"}
options.add_experimental_option("prefs", prefs)
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
    RealFileName = "HISTDATA_COM_NT_"+paire+"_T_BID"+an+mois+".zip"

    driver.get(URL)

    toclic = driver.find_element_by_link_text(FileName) #le nom de fichier est l'objet clicable
    notseen = True
    while (notseen):
        notseen =False
        try:
           toclic.click()
        except selenium.common.exceptions.ElementNotVisibleException :
            notseen = True
        except selenium.common.exceptions.WebDriverException :
            notseen = True


    pathdownload = "c:/tmp/"+RealFileName #attention le nom est different entre le zip et le lien clic

    #ici on attend la fin du telechargement
    notfound = True
    while (notfound):
        if os.path.exists(pathdownload):
            notfound = False

    print("found")
    # on cherche dans le zip un fichier csv
    #on le decompress dans tmp
    #puis on enleve le zip
    notok = True

    while notok:
        try:
            with zipfile.ZipFile(pathdownload, 'r') as zf:
                print (zf.filelist)
                for i in zf.filelist:
                    if i.filename.find(".csv") != -1 :
                        print("extract dans c:\\tmp : ",i.filename)
                        newpath = zf.extract(i,path="c:/tmp")
                        print('new path ',newpath, 'rename to',"c:\\tmp\\"+paire+".csv")
                        os.rename(newpath,"c:\\tmp\\"+paire+".csv")
                        notok = False

                zf.close()

        except PermissionError:
            #zf.close()
            if os._exists("c:\\tmp\\" + paire + ".csv"):
                os.remove("c:\\tmp\\" + paire + ".csv")
            print('redo')


    os.remove(pathdownload)

    return newpath,"c:\\tmp\\"+paire+".csv"



def liremois(mois,annee,listepairs):

    listefic = []  # liste des fichier extraits
    #on efface tous les csv du repetroire
    for todel in os.listdir("c:\\tmp"):
        if '.csv' in todel:
            os.remove("c:\\tmp\\"+todel)

    for pairename in listepaires :
        print ("lecture de :",pairename)
        dezipname,fichname = loadpairemoisan(pairename, mois, annee) #deux arguments en retrou, le 2eme est le nom actuel du fichier
        listefic.append(fichname) #liste des csv fabriques

    #on refusionne tout dans un zip du mois
    zipoutname = "c:\\tmp\\"+"BID"+mois+annee+".zip"
    zfileout = zipfile.ZipFile(zipoutname, 'w')
    for ficname in listefic:
        print("zip :",ficname," dans", zipoutname )
        inzipname = os.path.relpath(ficname,"c:\\tmp")
        print(inzipname)
        zfileout.write(ficname,inzipname) # on ne garde qu e le nom fichier on vire le path
        print('--- effacement de ',ficname,' ----------')
        os.remove(ficname)

    zfileout.close()
    return zipoutname

#ici le main
#listemois=["01","02","03","04","05","06","07","08","09"]
annee="2015"
listemois=["01"] #,"03","04","05","06","07","08","09","10","11","12"]
listepaires=["EURUSD","EURCHF","EURGBP","EURJPY","USDCAD","USDCHF","USDJPY","GBPCHF","GBPUSD","AUDUSD","EURCAD"]


#antidemarrage en librrairie
if __name__ == "__main__":
    # le programme principal
    for mois in listemois:
        liremois(mois,annee, listepaires)

