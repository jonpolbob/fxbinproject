import pandas as pd
import numpy as np

# toutes sortes de calculs sur le dataframe


#calcul des bolinger doubles
#cette fonction sort les 4 bollineger de tous les points de la table pdtable
def calcbolingerreduced(pdtable,params):#calcul de bolinger
    length=params[0]
    hinumsd=params[1]
    lownumsd = params[2]

    ave = pdtable[2].rolling(center=True,window=length).mean()
    #sd = pd.stats.moments.rolling_std(pdtable,length)
    sd = pdtable[2].rolling(center=True,window=length).std()
    upband = ave + (sd*hinumsd)
    dnband = ave - (sd*hinumsd)
    upband80 = ave + (sd * lownumsd)  #80% de bollinger dnband80 = ave - (sd * lownumsd)

    return upband,dnband,upband80,dnband80

#calcul des bolinger normaux
def calcbolinger(pdtable):#calcul de bolinger
    length=30
    numsd=2.0

    ave = pdtable[2].rolling(center=True,window=30).mean()
    #sd = pd.stats.moments.rolling_std(pdtable,length)
    sd = pdtable[2].rolling(center=True,window=30).std()
    upband = ave + (sd*numsd)
    dnband = ave - (sd*numsd)

    return upband,dnband

# calcule un bollinger avec une longueur et un ecart type different du normal
def calcmm80(pdtable):#calcul de bolinger
    length=80
    numsd=2.0

    ave = pdtable[2].rolling(center=True,window=length).mean()
    #sd = pd.stats.moments.rolling_std(pdtable,length)
    #sd = pdtable[2].rolling(center=True,window=30).std()
    return ave



#detecte une zone interessante dans un dataframe de candle
#sort une liste des index qui marchent
#super bourrin pour que ca marche
#pdtable est une table panda a 1 colonne
#la liste en sortie contient l'indice de la premiere candle de la zone detectee
#checkfifo  ^0 ne calcule que ke fait que un des open de l'esemble de détéction ne dépasse le low du début
def checkfifo0(lafifo):
    valeurdeb = lafifo[0][1][0]  # ohlc : on prend le open
    idxdeb = lafifo[0][0]  # index de la mesure

    Found = True
    # test aucune descente (low en dessous du begin)
    for i in lafifo:
        if (valeurdeb > i[1][2]):  # il faut pas que un low de l'ensemble soit < ouverture
            Found = False
            break
  # on n'a aucun point dans la fifo plus petit que la valeur
    # donc c'est ok
    # n ne detecte rien qui ne soit pas paeres 10 valeurs
    # il faut un peu de donnees dans le passe (par ex 10) pour pouvoir detecter un evenent

    return Found and idxdeb > 10,idxdeb

#checkfifo1 verifie que open-close est une montée pendant 4 candles
#et que la montée est toujours supérieure a 10 de la précédente
#enfin on vérifie cue le 5eme  est une descente
def checkfifo1(lafifo):
    valeurdeb = lafifo[0][1][0]  # ohlc : on prend le open
    idxdeb = lafifo[1][0]  # index de la mesure

    Found = True

    #on cherche une croissance de plus de l moitie de chaque barre
  #  increase1 = lafifo[0][1][3] - lafifo[0][1][0]  #open - close
 #   if (increase1 <0):
 #       return False,idxdeb #echec
    increase2 = lafifo[1][1][3] - lafifo[1][1][0]
    if (increase2 < 0):
        return False, idxdeb  # echec
  #  if (increase2 < increase1/10) :
  #      return False, idxdeb  # echec

    increase3 = lafifo[2][1][3] - lafifo[2][1][0]
    if (increase3 < 0):
        return False, idxdeb  # echec
    if (increase3 < increase2 / 10):
        return False, idxdeb  # echec

    increase4 = lafifo[3][1][3] - lafifo[3][1][0]
    if (increase4 < 0):
        return False, idxdeb  #
    if (increase4 < increase3 / 10):
        return False, idxdeb  # echec

    increase5 = lafifo[4][1][3] - lafifo[4][1][0]
    if (increase5 >0) :
        return False,idxdeb

    #on n'a aucun point dans la fifo plus petit que la valeur
    # donc c'est ok
    # n ne en qui ne soit pas paeres 10 valeurs
    # il faut un peu de donnees dans le passe (par ex 10) pour pouvoir detecter un evenent

    return True and idxdeb > 10,idxdeb




#-------------------------------------------------------------------------------------
#  les detectonteressant generent une liste des points de debut de sequneces qui marchent , les 4 valeurs sorties sont :
# les positions en x des séquences qui marchent ,
# resuy est le seuil stop a poser
# il faut sans doute modifier ctte valeur seuil dans tous ces calculs
# les points z ou il faudra afficher les marques et le count du nb de marques
#-------------------------------------------------------------------------------------

#nouvel essai ou on detecte 3 canle sur 5 sont des montees et traversent une des lilmllites des bool,
# et la derniere candle, la eme est une descente
#le seuil stop choisi est la bollinger aute(?)
def detectinteressantboll(pdtable,curves):
    bolhi = curves[0]
    bollo = curves[1]
    bolhiba = curves[2]
    bollohi = curves[3]
    moy80 = curves[4]

    resuX=[] #tableau des index
    resuOK=[]   #tableau des seuils ok
    resuSTOP = [] #tableau des seuils stop
    count=0

    for idx,lacandle in pdtable.iterrows():
        linelist = lacandle.values.tolist()
        found = True
        open = linelist[0] #open
        close = linelist[3] #close
        bollhimax = bolhi[idx]
        bollhimin = bolhiba[idx]
        mmval = moy80[idx]
        if (mmval < bollohi[idx]): #moyenne en dessous de bollinger bas
            found =False
        if (mmval > bolhiba[idx]): #moyenne en dessous de bollinger bas
            found =False

        if open <= bollhimin:  #commence en dessous de bol hi bas : pas bon
            found=False
        if close >= bollhimin:  # finit au dessus de bol hi bas : pas bon
            found = False

        if found:
            resuX.append(idx)
            resuOK.append(mmval)  #seil accepte gain
            resuSTOP.append(bollhimax) #seuil abandon
            count = count + 1

    return resuX,resuOK,resuSTOP,count


# cette detection utilise des bolinger modifiézs recherche une sequence de 3 candles situes entre les bolinger sans passer en dessous
#il faut que top et low soient entre les bolinger et bolinerhigh, ou top au dessus
# puis une descete
# en sortie : inex de la sequence detecteee
# seuils ok et stop a utiliser
#nombre de sequences trouvees dans cette semaine
#RESULTAT ca marche un peu avec des boli bien larges (0 pour moyenne, 2.4 et 0.8)
def detectinteressantbol4(pdtable,curves):
    bolhi = curves[0] #up
    bollo = curves[1]#dn
    bolhiba = curves[2]#up80
    bollohi = curves[3] #dn80
    moy80 = curves[4]

    resuX = []  # tableau des index
    resuOK = []  # tableau des seuils ok
    resuSTOP = []  # tableau des seuils stop
    count = 0
    dafifo = []
    histogram = [0,0,0,0]

    nbok =0
    for idx, lacandle in pdtable.iterrows():
        found = False
        linelist = lacandle.values.tolist()
        leopen = lacandle[0]  # open #le premier element de la fifo est une candle
        lehigh = lacandle[1]  # high
        lelow = lacandle[2]  # low
        leclose = lacandle[3]  # close

        lebolhi = bolhi[idx]
        lebolbas= bolhiba[idx]
        lamoy = moy80[idx]

        found =False


        #detecte une descente apres une sequence ok
        #avec une close en dessous de la bolinger basse
        if nbok == 3 and leopen > leclose and leclose < lebolbas :  #ok on a fini la sequence
            found=True

        if leclose < lebolbas :  #on repasse en dessous : on interrompt la sequence
            histogram[nbok]+=1
            nbok = 0

        if leopen <= leclose and leopen >= lebolbas and leclose <= lehigh :
            nbok  += 1
            if nbok >3:
                nbok = 3

        if found:
            resuX.append(idx)
            resuOK.append(lehigh) #valeur de stop a utiliser apres cette sequence
            resuSTOP.append(leclose) #valeur de OK a utiliser apres cette sequence
            count = count + 1

    print("nb item found ", len(resuSTOP))
    print("histogram",histogram)
    #on retourne la liste des index detectes, la veleur de deppart de la sequence (car il v=faut mettre un seul pour le calcul de la reussite/echec
    # et la valeur z pour la marque
    return resuX, resuOK, resuSTOP, count


#curvves = upbol dnbol, upbol80 , dnbol80, mm80
#cette detection recherche 3 candle parmi 5 qui sont en motee, et a cheval sur une lin de bolinger, et ensuite une descente
#resultat : caca detecte RIEN, meme avec des bolingers tres lrges

def detectinteressantbol3(pdtable,curves):
    bolhi = curves[0] #up
    bollo = curves[1]#dn
    bolhiba = curves[2]#up80
    bollohi = curves[3] #dn80
    moy80 = curves[4]

    resuX=[] #tableau des index
    resuOK=[]   #tableau des seuils ok
    resuSTOP = [] #tableau des seuils stop
    count=0
    dafifo = []

    for idx,lacandle in pdtable.iterrows():
        found=False
        linelist = lacandle.values.tolist()
        dafifo.append([linelist,bolhi[idx],bolhiba[idx],moy80[idx]])
        if len(dafifo)<=6:
            continue #on lit une ligne de plus, pas de detection

        #reduction de la fifo
        dafifo = dafifo[1:]
        countok = 0

        prvlow = dafifo[0][0][0] #open d 1er candle

        for lesdata in dafifo[:-1]:
            leopen = lesdata[0][0]  # open #le premier element de la fifo est une candle
            lehigh = lesdata[0][1]  # high
            lelow = lesdata[0][2]  # low
            leclose = lesdata[0][3]  # close
            bollhimax = lesdata[1]
            bollhilow = lesdata[2]
            lamoy80=lesdata[3]  #34eme element de la ffio

            ok = False
            # teste si openclose a cheval sr les limites des bol
            if leopen < bollhilow and leclose > bollhilow and leclose <  bollhimax :
                ok = True
            if leopen > bollhilow and leopen<  bollhimax and leclose > bollhimax :
                ok = True

          #  if prvlow < leopen:
           #     ok = False # pas d'increent de countok car c'est pas bon pour ce candle la

            prvlow = leopen  #pour le prochain tour

            if ok:
                countok += 1
            #test s open et close dans la bande
            #if open > bollhimax and close < bollhilow and open > close:
            #   ok = True

        if countok > 3 : #au moi s 3 sont ok
            #on regarde le final
            datafinal = dafifo[-1]
            leopen = datafinal[0][0]  # open
            lehigh = datafinal[0][1]  # high
            lelow = datafinal[0][2]  # low
            leclose = datafinal[0][3]  # close
            bollhimax = datafinal[1]
            bollhilow = datafinal[2]
            marqueurm80 = datafinal[3]

            if leclose < bollhilow and leopen < bollhimax and leopen > leclose:
                found = True

        if found:
            resuX.append(idx)
            resuOK.append(marqueurm80)
            resuSTOP.append(bollhimax)
            count = count + 1

    print("nb item found ",len(resuSTOP))
    return resuX, resuOK, resuSTOP, count

#fait la liste des points interessants
# on sort un tableau contenant les index des points interessants
def detectinteressant(pdtable,curves): #calcul de bolinger
#    return detectinteressant0(pdtable)
    return detectinteressantbol4(pdtable,curves)

#detectinteessant sur une fifo de 10


def detectinteressant0(pdtable):
    lafifo =[]
    resuX=[]
    resuY = []
    count=0

    #pour iterer sur les lignes de pandas il faut faire iterrows.
# on dirait que  un simle iteratuer renvoie des scalaires
    for idx,lacandle in pdtable.iterrows():
        linelist = lacandle.values.tolist()

        #on cree la fifo
        lafifo.append([idx,linelist])

        if (len(lafifo) > 10):
            found,ix = checkfifo1(lafifo)

            lafifo.pop(0) #on vire la valueur de reference, on travaille sur le reste de la pile

            if found : #on affichera une marque devant le debut
                resuX.append(ix)
                count=count+1

    return resuX,count





#clcul des resultats des evenements detectes
#les arguments sont : les candles
#la liste des index et des vleurs au declechement
#les courbes lissees
def calcresu(pdtable,tabidx,tabval,curves):
    pip = 3
    bolbas = curves[3]
    cntwin =0
    cntloose=0

    for leidx,lavaleur in zip(tabidx,tabval):
        maxval = 0  #valeur atteinte maxi
        minval=999999
        count =0
        Encore = True
        curidx = leidx

        while(Encore):
            count +=1
          #  print(pdtable.iloc(curidx))
            candle2 = pdtable.iloc[curidx,2]
            candle1 = pdtable.iloc[curidx,1]
            maxval = max(maxval,candle1) #max
            minval = min(minval,candle2)
            if (candle2 < bolbas[curidx]):   #on arrete qd le min est asse sous le bol du bas
                cntwin +=1
                print("win val= ",lavaleur, "max atteint =",maxval, "cunt=", count)
                break

            if (candle1>lavaleur+pip*.0001): #rate a +3pip
                cntloose +=1
                print("loose val= ", lavaleur, "  min atteint= ", minval, "(maxcancel = ",candle2,"pour ",lavaleur+pip*.0001,") count=", count)

                break;

            curidx = curidx+1
            if (curidx >= len(pdtable)):
                break

    print ("win:",cntwin,"  loose : ",cntloose)