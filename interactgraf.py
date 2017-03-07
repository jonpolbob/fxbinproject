

import matplotlib.pyplot as plt
import matplotlib as mp

plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

fibo = 1
lstfibo =2

x = []
toupdate =0
y=[]

def update2(lavaleur):
    global toupdate, x, y, ax1, fig
    if len(x) < 30 :
        x.append(len(x)+1)
    y.append(lavaleur)
    if len(y) >30:
        y.remove(y[0])

    toupdate =1
    #y1=[valcible,valcible]
    #y2 = [valcancel, valcancel]
    #y3 = [lavaleur, lavaleur]

def updategraph(valcible,valcancel):
    global toupdate, x, y, ax1, fig

    if toupdate ==0:
        return

    toupdate =0

    if len(y)==0:
        return

    ydraw=[]

    for valeur in y:
        ydraw.append([valcible,valcancel,valeur])

    ax1.cla()
    ax1.plot(x,ydraw)
    fig.canvas.update()
    fig.canvas.flush_events()
    fig.show(False)


def update():
    global x
    global ax1
    global fibo
    global lstfibo

    x.append(x[-1]+1)
    y=[]
    for truc in x:
        toadd = lstfibo
        lstfibo = fibo
        fibo = toadd + fibo
        y.append(fibo)

    ax1.cla()
    ax1.plot(x,y)
    fig.canvas.update()
    fig.canvas.flush_events()
    fig.show(False)

