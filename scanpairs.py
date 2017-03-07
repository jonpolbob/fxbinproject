from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile
import ntplib,datetime
import time
import threading

import interactgraf

from ctypes import *

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

STD_OUTPUT_HANDLE = -11
h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


pairs = ["eurusd", "usdjpy", "audusd", "gbpusd", "usdcad", "nzdusd", "audcad", "audchf", "audjpy", "eurchf", "eurgbp",
         "eurjpy", "usdchf"]

trackpaire = "eurusd"
valcible =0
valcancel =0
SellOrBy=False
affich=1
lstval = 0

opval = []
clval = []
maxval = []
minval = []
ladate = []

def initall():
    global opval
    global clval
    global maxval
    global minval
    global ladate
    newdate = datetime.datetime.now()

    for paire in pairs:
        ladate.append(newdate)
        opval.append(-1)
        clval.append(-1)
        maxval.append(-1)
        minval.append(999999)


def initcandle(paire,date):
    global pairs
    global opval
    global clval
    global maxval
    global minval
    global ladate
    global affich

    idx = pairs.index(paire)
    if (affich==1 and opval != -1): #il y a des valeurs
        print(paire," ",ladate[idx].hour,":",ladate[idx].minute,':','O=',opval[idx],'H=',maxval[idx],'L=',minval[idx],'C=',clval[idx])

    ladate[idx] = date
    opval[idx] = -1
    clval[idx] = -1
    maxval[idx] =-1
    minval[idx] = 9999

def candlelize(paire,valeur):
    global pairs
    global opval
    global clval
    global maxval
    global minval

    idx = pairs.index(paire) #retrouve unun index par sa valeur

    if opval[idx] == -1:
        opval[idx]=valeur
    clval[idx] = valeur
    if maxval[idx] < valeur:
        maxval[idx] = valeur
    if minval[idx] > valeur:
        minval[idx] = valeur

    return


def scanweb(timeout):
    global pairs
    global valcible
    global valcancel
    global SellOrBy
    global h,affich
    global lstval

    # personalisation des options(rep de download et adresse vers chromdriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "c:/tmp"}
    options.add_experimental_option("prefs", prefs)
    chromedriver = "c:/windows/system32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.set_page_load_timeout(timeout)
    URL = "https://www.dailyfx.com/forex-rates"

    driver.get(URL)

    Encore=True

    lstvalbid = []
    lstvalask = []

    #init les valeurs
    for lapaire in pairs:
        lstvalbid.append(-1)
        lstvalask.append(-1)
        minval.append(9999999)
        maxval.append(-1)
        opval.append(-1)
        clval.append(-1)

    x = ntplib.NTPClient()

    lstmin = -1


    while Encore:
        windll.kernel32.SetConsoleCursorPosition(h, COORD(1, 15))

        debclock = time.clock()
        ladate = datetime.datetime.now() #.getnow() #datetime.utcfromtimestamp(x.request('europe.pool.ntp.org').tx_time)
        if ladate.minute != lstmin:
            for paire in pairs:
                initcandle(paire,ladate)
            lstmin = ladate.minute
            print(" -- ", ladate.hour, ":", ladate.minute, ":", ladate.second)


        for idx,lapaire in enumerate(pairs):
            towrite =0
            id=lapaire+"-priceBid"
            valeurbid = driver.find_element_by_id(id)
            if valeurbid == None:
                continue
            if (valeurbid.text == '---'):
               continue
            valbid=float(valeurbid.text)
            if (valbid != lstvalbid[idx]):
                towrite = 1
                lstvalbid[idx] = valbid
                candlelize(lapaire,valbid)


            id = lapaire + "-priceAsk"
            valeurask = driver.find_element_by_id(id)
            if valeurask == None:
                continue
            if (valeurask.text == '---'):
                continue

            valask = float(valeurask.text)
            if (valask != lstvalask[idx]):
                towrite = 1
                lstvalask[idx] = valask
                if (trackpaire == lapaire):
                    lstval=valask
                    interactgraf.update2(valask)
                    if (SellOrBy):
                        if (valask > valcancel):
                            print("CANCEL")

                        if (valask < valcible):
                            print("ACCEPT")

                    else:
                        if (valask > valcible):
                            print("ACCEPT")

                        if (valask  < valcancel):
                            print("CANCEL")

                        #candlelize(lapaire, valbid)on candlelize sur le ask

            if (affich ==1 and towrite != 0 ):
                print(" lapaire :", lapaire,r"/", valbid,"/",valask)

        finclock = time.clock()
        duration = finclock-debclock
        print("---------------------- dur=",duration)
        if duration < .50:
            time.sleep(.50-duration)



#le main

class webThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        scanweb(120)

import colorama  #pour emulation terminal ansi

#pour xy positionnement console


initall()
lethread = webThread(1,"scanthread",1)
lethread.start()
Command=1

import sys
import os
import msvcrt
import time


while Command !=0:

    os.system('cls')
    windll.kernel32.SetConsoleCursorPosition(h, COORD(1, 1))

    print("s: seuil reject",valcancel)
    print("a: seuil accept",valcible)
    print("x: achat/vente","Sell" if SellOrBy else "Buy")

    print("p: paire track (",trackpaire,")")

    interactgraf.update2(lstval)
    affich = 1
    a=""
    print("cmd?")
    while a=="":
        if msvcrt.kbhit():
            a=input()
        else:
            interactgraf.updategraph(valcible,valcancel)
        time.sleep(0.1)

    affich=0
    os.system('cls')
    if a=='q':
        Command=0

    try:

        if a=='s':
            print ('cancel=',valcancel)
            a = input ("nouveau seuil ?")
            if a=="":
                continue
            valcancel = float(a)

        if a == 'a':
            print('accept=',valcible)
            if (SellOrBy):
                a = input("nouveau seuil ARRET (min) ?")
            else:
                a = input("nouveau seuil VALID (max) ?")

            if a == "":
                continue

            valcible = float(a)

    except ValueError:
        continue

    if a == 'x':
        print('Sell/Buy=',)
        if (SellOrBy):
            print('sell')
        else:
            print('buy')
        a = input("nouveau sens (s/b)?")
        if a=='s':
            SellOrBy =True
        if a == 'b':
            SellOrBy = False

    if a=='p':
        for index,current in enumerate(pairs):
            print(index,":",current)

        a = input("paire ?")
        if a == "":
            continue
        trackpaire = pairs(int(a))



