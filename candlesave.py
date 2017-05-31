
from threading import Thread
 #modeul sauvagardant les candle d'une minute sous thread dans des fichiers


# Start running the threads!


import queue
import time
import csv

class MyThread(Thread):
    q=None

    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)
        self.q = queue.Queue()


    def pushresu(self, semaine,minute,paire,nbmesures,open,top, low, close):
        i=[semaine,minute,paire,nbmesures,open,top, low, close]
        if (self.q != None):
            self.q.put(i)


    def run(self):
        Encore = True
        while (Encore):
            while not self.q.empty():
                i = self.q.get()
                print(i)
                #print('Value %d in thread %s' % (i, self.getName()))
                #filename = i[2]+String(i[1])+String(i[0])+".csv"
                filename = i[2] + '%0*d' % (3, i[1]) +"-"+ '%0*d' % (3, i[0])+".csv"
                print(filename)
                with open(filename,'a') as csvfile:
                    spamwriter = csv.writer(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)

                    spamwriter.writerow(i)
                    csvfile.close()

            time.sleep(1)