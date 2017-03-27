
#pour la lecture des heures du net
import ntplib
from time import ctime

x = ntplib.NTPClient()

def getdattime():
    response = x.request('europe.pool.ntp.org', version=3)
    return ctime(response.tx_time)

