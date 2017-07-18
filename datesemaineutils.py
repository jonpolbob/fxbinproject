#toutes sortes d'utils pour lire et calculer les dates , minutes et jours de semaine

import datetime

##################################################"
##utilitaire renvoyant tous les elements d'une date
#time est un datetime
##################################################"
def decodetime(time):
    letuple = time.timetuple()

    day = letuple.tm_day()
    hour = letuple.tm_hour()
    minute = letuple.tmmin()
    weekday = letuple.wday()
    return day,hour,minute,weekday


# ---------- decode une ligne de fichier csv ------------------
# renvoie
# #le nb minutes depuis debut du mois (1er du mois 0:00)
# la date
# la valeur de begin
#fonctionne pour une ligne de csv separre par ; contenant la date yyyymmdd hhmmss suvie dans le champ 0
def decodelinemois(laligne):
    colonnes = laligne.split(b';')
    return decodesplittedline(colonnes)

def decodesplittedline(colonnes):
    # print (colonnes)
    ladate = colonnes[0]
    annee = int(ladate[0:4])
    mois = int(ladate[4:6])
    jour = int(ladate[6:8])
    heure = int(ladate[9:11])
    minute = int(ladate[11:13])
    secondes = int(ladate[13:15])
    datenumber = datetime.datetime(year=annee, month=mois, day=jour, hour=heure, minute=minute, second=secondes)
    datenumberdebut = datetime.datetime(year=annee, month=mois, day=1, hour=0, minute=0, second=0)
    deltatime = datenumber - datenumberdebut
    deltamins = int(deltatime.total_seconds()/60)

    beginvalue = colonnes[1]

   #deltamins = nb minutes depuis debut du mois
   #datenumber = la date-heure de cette mesure
    return deltamins, datenumber, float(beginvalue)


############ getdimanchefromweek ###############################
#renvoie la date du dimanche en debut de seamine (les semaines commencent un dimanche)
def getdimanchefromweek(semaine,annee):
    d = str(annee)+"-"+str(semaine).zfill(2)+"-1"
    r = datetime.datetime.strptime(d, "%Y-%W-%w") #on a la date du lundi
    rp = r-datetime.timedelta(1) #1 jour
    #print(r,rp)
    return rp.year,rp.month,rp.day

############ getsamedifromweek ###############################
#renvoie le dernier jour de la semaine
def getsamedifromweek(semaine,annee):
    d = str(annee) + "-" + str(semaine).zfill(2) + "-1"
    r = datetime.datetime.strptime(d, "%Y-%W-%w")  # on a la date du lundi
    rp = r + datetime.timedelta(6)  # +6 jour du lundi = le samedi
    return rp.year,rp.month,rp.day

