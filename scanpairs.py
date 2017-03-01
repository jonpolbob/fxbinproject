from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile
import ntplib,datetime


# personalisation des options(rep de download et adresse vers chromdriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "c:/tmp"}
options.add_experimental_option("prefs", prefs)
chromedriver = "c:/windows/system32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

URL = "https://www.dailyfx.com/forex-rates"

driver.get(URL)

Encore=True

pairs=["eurusd","usdjpy","audusd","gbpusd","usdcad","nzdusd","audcad","audchf","audjpy","eurchf","eurgbp","eurjpy","usdchf"]
lstval = []
opval = []
clval=[]
maxval=[]
minval=[]

#init les valeurs
for lapaire in pairs:
    lstval.append(-1)
    minval.append(9999999)
    maxval.append(-1)
    opval.append(-1)
    clval.append(-1)

x = ntplib.NTPClient()

lstmin = -1

def savecandles():
    return



while Encore:
    ladate = datetime.utc() #.getnow() #datetime.utcfromtimestamp(x.request('europe.pool.ntp.org').tx_time)
    if ladate.min != lstmin:
        savecandles()
        lstmin = ladate.min

    for lapaire in pairs:
            id=lapaire+"-priceBid"
            valeur = driver.find_element_by_id(id)
            print(ladate.hour,":",ladate.min,":",ladate.second," lapaire :",id, "valeur:",valeur.text)






