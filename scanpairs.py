#programme princpal de lecture des paires en live sur pc
#lit les paires en live
#utilise readwebwindows pour selenium
#le scan est dans un thread a part, ce qui permet de gerer l'interface utilsateur pendant le scan
#une paire speciale (trackpaire) est analysee dfferemment
# les autres generent des candles
#winconsole permet l'ffichae de commentaires suiivante l'ordi qui execute

import datetime
import threading

import interactgraf
import readwebwindows
import timserver
from archive import winconsole

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

#initialisation d'une candle en debut de semaine
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
        winconsole.Xprint(paire, " ", ladate[idx].hour, ":", ladate[idx].minute, ':', 'O=', opval[idx], 'H=', maxval[idx], 'L=', minval[idx], 'C=', clval[idx])

    ladate[idx]=date
    opval[idx] = -1
    clval[idx] = -1
    maxval[idx] =-1
    minval[idx] = 9999

#ajoute une nouvelle valeur a une candle
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

#fonction du thread
#lit les valeurs du web. quand une valeur change -> on met a jour la liste des valeurs
def scanweb(timeout):
    global pairs
    global valcible
    global valcancel
    global SellOrBy
    global h,affich
    global lstval

    driver = readwebwindows.init()   # a modifier pour linux

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


    lstmin = -1

    curnbupdates = 0

    while Encore:
        winconsole.setxy(1, 15)

        debclock = time.time()
        ladate = datetime.datetime.now() #.getnow() #datetime.utcfromtimestamp(x.request('europe.pool.ntp.org').tx_time)
        if ladate.minute != lstmin:
            for paire in pairs:
                initcandle(paire,ladate)
            lstmin = ladate.minute
            winconsole.Xprint(timserver.getdattime(), "nb upd =", curnbupdates)
            curnbupdates = 0

            winconsole.Xprint(" -- ", ladate.hour, ":", ladate.minute, ":", ladate.second)

        curnbupdates = curnbupdates+1
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
                    winconsole.setxy(1, 6)
                    winconsole.Xprint("current : ", lstval, " cmd?")

                    interactgraf.update2(valask)
                    if (SellOrBy):
                        if (valask > valcancel):
                            winconsole.Xprint("CANCEL")

                        if (valask < valcible):
                            winconsole.Xprint("ACCEPT")

                    else:
                        if (valask > valcible):
                            winconsole.Xprint("ACCEPT")

                        if (valask  < valcancel):
                            winconsole.Xprint("CANCEL")

                        #candlelize(lapaire, valbid)on candlelize sur le ask

            if (affich ==1 and towrite != 0 ):
                winconsole.Xprint(" lapaire :", lapaire, "/", valbid, "/", valask)

        finclock = time.time()
        duration = finclock-debclock
        winconsole.Xprint("---------------------- dur=" + duration)
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


#pour xy positionnement console


initall()
lethread = webThread(1,"scanthread",1)
lethread.start()
Command=1

import time

a="$" #pour faire le 1er rafraichissement

while Command !=0:
    if a != "":
        winconsole.cls()
        winconsole.setxy(1, 3)

        winconsole.Xprint("s: seuil reject", valcancel)
        winconsole.Xprint("a: seuil accept", valcible)
        winconsole.Xprint("x: achat/vente", "Sell" if SellOrBy else "Buy")

        winconsole.Xprint("p: paire track (", trackpaire, ")")

        interactgraf.update2(lstval)
        affich = 1

        winconsole.setxy(1, 1)
        winconsole.Xprint("current : ", lstval)
    a=""

    while a=="":
        if winconsole.Xkbhit():
            a= winconsole.Xinput("")  #xprint a besoin d'un argument
        else:
            if interactgraf.updategraph(valcible,valcancel) ==1:  #il y a eu une mise a jour -> changemetn de valeur
                a="$" #commande bidon, juste pour rafraichir
            else:
                time.sleep(0.1)

    affich=0
    #os.system('cls')
    if a=='q':
        Command=0

    try:

        if a=='s':
            winconsole.setxy(1, 1)
            winconsole.Xprint ('cancel=', valcancel)
            a = winconsole.Xinput ("nouveau seuil ?")
            if a=="":
                a = "$"
                continue
            valcancel = float(a)

        if a == 'a':
            winconsole.setxy(1, 1)
            winconsole.Xprint('accept=', valcible)
            if (SellOrBy):
                a = winconsole.Xinput("nouveau seuil ARRET (min) ?")
            else:
                a = winconsole.Xinput("nouveau seuil VALID (max) ?")

            if a == "":
                a = "$"
                continue

            valcible = float(a)

    except ValueError:
        a="$"
        continue

    if a == 'x':
        winconsole.setxy(1, 1)
        winconsole.Xprint('Sell/Buy=', )
        if (SellOrBy):
            winconsole.Xprint('sell')
        else:
            winconsole.Xprint('buy')
        a = winconsole.Xinput("nouveau sens (s/b)?")
        if a=='s':
            SellOrBy =True
        if a == 'b':
            SellOrBy = False

    if a=='p':
        winconsole.cls()
        winconsole.setxy(1, 3)

        for index,current in enumerate(pairs):
            winconsole.Xprint(index, ":", current)

        winconsole.setxy(1, 1)
        a = winconsole.Xinput("paire ?")
        if a == "":
            continue
        trackpaire = pairs[int(a)]



