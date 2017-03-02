from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile
import ntplib,datetime
import time
import threading


pairs = ["eurusd", "usdjpy", "audusd", "gbpusd", "usdcad", "nzdusd", "audcad", "audchf", "audjpy", "eurchf", "eurgbp",
         "eurjpy", "usdchf"]


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

    idx = pairs.index(paire)
    if (opval != -1): #il y a des valeurs
        print(paire," ",ladate[idx],':','O=',opval[idx],'H=',maxval[idx],'L=',minval[idx],'C=',minval[idx])

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
        debclock = time.clock()
        ladate = datetime.datetime.now() #.getnow() #datetime.utcfromtimestamp(x.request('europe.pool.ntp.org').tx_time)
        if ladate.min != lstmin:
            for paire in pairs:
                initcandle(paire,datetime)
            lstmin = ladate.min

        for idx,lapaire in enumerate(pairs):
            towrite =0
            id=lapaire+"-priceBid"
            valeurbid = driver.find_element_by_id(id)
            if valeurbid == None:
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
            valask = float(valeurask.text)
            if (valask != lstvalask[idx]):
                towrite = 1
                lstvalask[idx] = valask
                #candlelize(lapaire, valbid)on candlelize sur le ask

            if towrite != 0 :
                print(ladate.hour, ":", ladate.minute, ":", ladate.second, " lapaire :", id, "valeur:", paire,r"/", valeurask.text)

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




initall()
lethread = webThread(1,"scanthread",1)
lethread.start()
a=input("stop?")

