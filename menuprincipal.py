#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'


def listoptions(laliste) :
    print("0 :  fin ")
    valeur =1
    if (len(laliste) ==0):
        return 0

    for item,numligne in enumerate(laliste) :
        print(numligne+1,": ",item)

    while (True) :
        option = getchoice(len(laliste))
        for item, numligne in enumerate(laliste):
            if (numligne == option-1):
                return numligne


#lit le clavier et regarde si valeur est dans les valeurs autorisees
def getchoice(lavalmax):

    while (True):  #tourne toujours
        choix = input("ton choix")

        try :
            choixint = int(choix)
        except:
            choixint = lavalmax  #pas un chiffre : on reboucle

        if choixint < lavalmax : #check si on est dans l'intervalle
            return choixint



        if choix == '1':
            print("option1")
            return 1
        if choix == '2':
            print("option2")
            return 2

option=1

while (option != 0):
    options = listoptions00(["option","option2","option3"])
    print ("option",option)

print ("c'est fini")

