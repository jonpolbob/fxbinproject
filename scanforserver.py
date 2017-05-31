import selenium
import readwebwindowserver
import readwebwindows

driver = readwebwindows.initwebwindows()
#driver = readwebwindowserver.initwebwindowsvr()
driver.get("http://www.dailyfx.com/forex-rates")
print(driver.title)

listitems = {"eurusd":[0,0,0,0,0,0,0],
			 "audusd":[0,0,0,0,0,0,0],
             "usdcad":[0,0,0,0,0,0,0],
             "gbpusd": [0,0,0,0,0,0,0],
             "usdjpy": [0,0,0,0,0,0,0],
             "usdchf": [0,0,0,0,0,0,0],
             "eurgbp": [0,0,0,0,0,0,0],
             "eurchf": [0,0,0,0,0,0,0],
             "eurjpy": [0,0,0,0,0,0,0],
             "gbpjpy": [0,0,0,0,0,0,0],
             "gbpchf": [0,0,0,0,0,0,0],
             "gbpcad": [0,0,0,0,0,0,0]
             }

Encore =True

from datetime import datetime, timezone, timedelta

def datprocess():
    #lecture heure du moment en utc
    nowhourutc = datetime.now(timezone.utc)

    #lecure heure en naive pour calculer les minutes au dimanche soir
    nowhour = datetime.now()
    nowTime = nowhour.strftime("%Y%m%d%H%M%S")
    leday = nowhour.weekday()
    #day =0 si lundi
    debsemaine =  nowhour-timedelta(leday+1) #date du lundi
    dimanchesoir = datetime(debsemaine.year,debsemaine.month,debsemaine.day,22,0,0) #dimanche soir 22h
    deltasecs = nowhour-dimanchesoir
    deltamin = deltasecs.total_seconds() /60
    deltahours = deltamin/60

    #calcul numero semaine
    numsem = dimanchesoir.isocalendar()[1]

    #print(nowTime, " ", dimanchesoir, "sem= ",numsem,")"," (", deltahours, ") ", deltamin)

    return nowhourutc,int(deltamin),numsem



def savepaires(minute):
    if minute == -1:
        return

    for curpair in listitems:
        lapaire  = curpair
        semaine = 0
        nbchangements = listitems[curpair][1] # nomre d'infos obtenues sur la minute
        openvalue =  listitems[curpair][3]
        highvalue =  listitems[curpair][4]
        lowvalue =  listitems[curpair][5]
        closevalue = listitems[curpair][6]
        #print(curpair," ",minute," ",nbchangements," ",openvalue,highvalue,lowvalue,closevalue)
        savethread.pushresu(semaine,minute, curpair,nbchangements,openvalue,highvalue,lowvalue,closevalue)
        listitems[curpair][1] =0# nomre d'infos obtenues sur la minute
        listitems[curpair][3] =closevalue
        listitems[curpair][4] =closevalue
        listitems[curpair][5] =closevalue
        listitems[curpair][6] =closevalue


import candlesave

savethread = candlesave.MyThread()
savethread.setName('Thread 1')
savethread.start()

lstmin=-1
lstsem = -1
lstcountmin=-1

while Encore == True:
    newtime = False#nouvelle tranche de minutes
    nowhour,countmin,sem = datprocess()
    if countmin != lstcountmin: #fin d'une minute
        print("--- ",countmin," ---")
        savepaires(countmin)
        newtime =True
    lstcountmin = countmin
    lstsemnum = sem

    for curpair in listitems:
        try:
            id=curpair+"-priceBid"
            valeurbid = driver.find_element_by_id(id)
            #nowTime = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
            #lheure,lesmins = datprocess()
            if valeurbid == None:
                continue
            if valeurbid.text == "---":
                continue

            floatvalue = float(valeurbid.text)
            if floatvalue != listitems[curpair][0]:
                listitems[curpair][0] = floatvalue
                if newtime : # la valeur de la candle vient de changer : on la remplce par les nouvelles valeurs
                    listitems[curpair][1] = 1  # nomre d'infos obtenues sur la minute
                    listitems[curpair][3] = floatvalue
                    listitems[curpair][4] = floatvalue
                    listitems[curpair][5] = floatvalue
                    listitems[curpair][6] = floatvalue
                else:
                    listitems[curpair][6] = floatvalue
                    listitems[curpair][4] = min(floatvalue,listitems[curpair][4])
                    listitems[curpair][5] = max(floatvalue, listitems[curpair][5])
                    listitems[curpair][1] += 1  # nomre d'infos obtenues sur la minute

                #print (nowhour,":",countmin,"|",sem,"-", curpair,valeurbid.text)
        except selenium.common.exceptions.NoSuchElementException:
            continue



