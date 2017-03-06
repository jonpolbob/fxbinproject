from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile
import ntplib,datetime
import time
import threading


pairs = ["eurusd", "audusd","usdcad"]
#""usdjpy", "audusd", "gbpusd", "usdcad", "nzdusd", "audcad", "audchf", "audjpy", "eurchf", "eurgbp",
 #        "eurjpy", "usdchf"]

upperpairs = []
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
    global upperpairs

    newdate = datetime.datetime.now()

    for paire in pairs:
        ladate.append(newdate)
        opval.append(-1)
        clval.append(-1)
        maxval.append(-1)
        minval.append(999999)
        upperpairs.append(paire.upper())


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
    global pairs,upperpairs

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
        if ladate.minute != lstmin:
            for paire in pairs:
                initcandle(paire,ladate)
            lstmin = ladate.minute

        from selenium.webdriver.common.by import By

        leselements = driver.find_elements_by_class_name("rates-row")
        for element in leselements:
            splittedelement = element.text.split()
            towrite = 0
            if splittedelement[1]=='---' or splittedelement[2]=='---':
                continue

            if splittedelement [0] in upperpairs:
                paire = splittedelement[0]
                idx = upperpairs.index(paire)

                valbid = float(splittedelement [1])
                if (valbid != lstvalbid[idx]):
                    lstvalbid[idx] = valbid
                    towrite = 1

                valask = float(splittedelement [2])
                if (valask != lstvalask[idx]):
                    towrite = 1
                    lstvalask[idx] = valask

                spread = float(splittedelement [3])
                if towrite ==1:
                    print(paire,":",valbid,"/",valask,"[",spread,"] @",ladate.hour,':',ladate.minute,":",ladate.second)
                    candlelize(pairs[idx],valask)


        finclock = time.clock()
        duration = finclock-debclock
        print("---------------------- dur=",duration)
        #if duration < .50:
        #    time.sleep(.50-duration)



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

