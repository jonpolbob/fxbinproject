#!/usr/bin/env python
# -*- coding: utf-8 -*-


import readweekpaire

import numpy as np
import pandas as pd
from matplotlib.finance import  candlestick_ohlc
import matplotlib.pyplot as plt
#34 2015 = 17 aout
#36 2015 : aout sept

letableau = readweekpaire.readweek(44, 2015, 'AUDUSD')
tabcandle = readweekpaire.candelize(letableau)
print(tabcandle)

table=np.zeros(7200)
for i in tabcandle:
   table[i[0]] = i[1]
print (table)

nantable = table[0:200]

nantable[:]=np.nan
pdtable = pd.DataFrame(nantable)
#pdtable = np.nan #init as nan
length=30
numsd=2.0
#ave = pd.stats.moments.rolling_mean(pdtable,length)
ave = pdtable.rolling(center=False,window=30).mean()
index = np.arange(0,len(ave))
#sd = pd.stats.moments.rolling_std(pdtable,length)
sd = pdtable.rolling(center=False,window=30).std()
upband = ave + (sd*numsd)
dnband = ave - (sd*numsd)

#tabcurves = np.column_stack([index[30:200],upband[30:200],dnband[30:200]])
#print (tabcurves[0:200])

#print(np.round(ave,3), np.round(upband,3), np.round(dnband,3))

# Plot two charts to assess trades and equity curve
fig = plt.figure()
fig.patch.set_facecolor('white')  # Set the outer colour to white
ax1 = fig.add_subplot(211, ylabel='Price in $')

# Plot the "buy" trades against
#ax1.plot(upband,'^', markersize=10, color)
#ax1.plot(upband,'^', markersize=10, color='m'
candlestick_ohlc(ax1, tabcandle, width=.8)
ax1.plot(index,upband,'^', ls='-', markersize=1, color='m')
ax1.plot(index,dnband,'^', ls='-', markersize=1, color='g')
plt.show()

