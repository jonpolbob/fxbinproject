#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'


# lecture sur hisdata.com d'un fichier de bid ou ask, pour un mois/annee donné
#pour septembre 2016 il faut lire
# http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9

# et provoquer le chargement de histdata_com_nt_eurusd_t_bid_201609.zip

from urllib.request import urlopen
from bs4 import BeautifulSoup


#htmlSource = urlopen("http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9")

#print (htmlSource.read())




sourcePage = urlopen('http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9')
soup = BeautifulSoup(sourcePage.read())

links = soup.find_all('a')

toclic = soup.find("a", { "id" : "a_file" })

print(toclic)

toclic.click()


#for link in links:
#    href = link['href']
#    print(href)
#    if '.zip' in href:

#        remoteZip = urlopen(href)
#        file_name = href.rpartition('/')[-1]
#        local_file = open(file_name, 'wb')
#        local_file.write(remoteZip.read())
#        local_file.close()


