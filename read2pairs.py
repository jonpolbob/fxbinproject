#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

# read2Pairs utilitaires pour lire 2 paires a la fois
# lit 2 paires et les apparie minute par minute

nomrep = "G:\\stockage\\fxdata\\"

#genere les noms de fichiers pour une paire
def gennomfichzip(mois, annee,dev1,dev2):
    iannee = int(annee)
    imois = int(mois)
    nomfich = nomrep+"HISTDATA_COM_ASCII_"+dev1+dev2+"_M1"+"%4d%02d"%(iannee,imois)+".zip"
    #nomfich2="dat_ascii_{0}{1}_M1_{2:4d}{3:02d}.csv".format(dev1,dev2,iannee,imois)
    #attention les majuscules comptent
    nomfich2="DAT_ASCII_{0}{1}_M1_{2:4d}{3:02d}.csv".format(dev1.upper(),dev2.upper(),iannee,imois)

    return nomfich,nomfich2  #,nomfichshort


import datetime
#decode une ligne de csv
#renvoie l'heure en datetime et la 1ere valeur
def decodeline(laligne):
     colonnes = laligne.split(b';')
     #print (colonnes)
     ladate = colonnes[0]
     annee = int(ladate[0:4])
     mois = int(ladate[4:6])
     jour = int(ladate[6:8])
     heure = int(ladate[9:11])
     minute = int(ladate[11:13])
     datenumber = datetime.datetime(year=annee, month=mois, day = jour, hour= heure, minute=minute)
     begin = colonnes[1]
     #print(ladate)
     #print (annee,mois,jour,heure,minute)
     #print(datenumber.year, datenumber.month, datenumber.day,datenumber.hour, datenumber.minute)
     #print (float(begin))
     return datenumber,float(begin)


import zipfile

def readfile(mois, annee, paire1A,paire1B, paire2A,paire2B):

    # extrait le fichier de data de dedans le zip
    #nomzip1, nomfich1 = gennomfichzip(2, 2014, "eur", "usd")
    #nomzip2, nomfich2 = gennomfichzip(2, 2014, "usd", "cad")
    nomzip1, nomfich1 = gennomfichzip(mois, annee, paire1A, paire1B)
    nomzip2, nomfich2 = gennomfichzip(mois, annee, paire2A, paire2B)


    fh1 = open(nomzip1, 'rb')
    z1 = zipfile.ZipFile(fh1) # classe lisant le zipdanzs le fichier ouvert


    fh2 = open(nomzip2, 'rb')
    z2 = zipfile.ZipFile(fh2) # classe lisant le zipdanzs le fichier ouvert


    count=0
    nxt1 =1
    nxt2 = 1
    stop=0
    val1=b""
    val2=b""

    with z1.open(nomfich1,mode = 'r') as read1:
        iter1 = read1.__iter__()
        with z2.open(nomfich2,mode ='r') as read2:
            iter2 = read2.__iter__()
            while stop == 0:

                try:
                    if (nxt1 == 1):
                        nxt1 = 0
                        val1  = iter1.__next__()
                        #print ("{",val1,"}")


                    if (nxt2 == 1):
                        nxt2 =0
                        val2 = iter2.__next__()
                    # print("[", val2, "]")

                except:
                    #nxt1=0
                    #nxt2=0
                    print("fin")
                    stop=1
                    pass

                date1,valeur1 = decodeline(val1)
                date2, valeur2 = decodeline(val2)

                # ---- meme date : c'est bon : on enregistre les 2 valeurs ----
                if (date1 == date2 ):
                    print(date1.day, date1.hour, date1.minute,valeur1,valeur2)
                    yield date1,valeur1,valeur2 #on envoie la valeur
                    nxt1 = 1
                    nxt2 = 1

                #pas meme date/heure : on lit le suivant de celui qui est en retard
                if (date1 < date2):
                    nxt1 = 1
                    nxt2 = 0

                if (date1 > date2):
                    nxt1 = 0
                    nxt2 = 1



for date,valeur1,valeur2 in readfile(2,2014,"eur","usd","usd","cad")
    print (date,valeur1,valeur2)
