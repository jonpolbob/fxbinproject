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

import sqlite3

db=None
#gestion sql
def initsql(listtables):
    db = sqlite3.connect("paires.db")
    for paire in listtables:
        c = db.cursor()
        c.execute('''CREATE TABLE tab_'+paire+'
                     (idx text, date text, op real, hi real, low real, cl real)''')
        nomtable="tab_"+paire








laqueue = queue.Queue()



