import queue
import threading
import time

#mey une candel dans la queue
def queueput(paire,date,indexminute,candle):
    Newval = [paire,date,indexminute,candle]
    laqueue.put(Newval)



def runqueue():
    Encore =True;

    while Encore:
        if laqueue.empty():
            time.sleep(1)
            continue
        Newval = laqueue.get()
        paire = Newval[0]
        date = Newval[1]
        minuteindex = Newval[2]
        candle=Newval[2]

import MySQLdb

db=None
#gestion sql
def initsql(listtables):
    public db
    db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB")
    for paire in listtables:
        nomtable="tab_"+paire








laqueue = queue.Queue()



