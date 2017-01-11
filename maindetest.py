#!/usr/bin/env python
# -*- coding: utf-8 -*-


import readweekpaire

import numpy as np
import pandas as pd
from matplotlib.finance import candlestick, plot_day_summary, candlestick2


#34 2015 = 17 aout
#36 2015 : aout sept

letableau = readweekpaire.readweek(44, 2015, 'AUDUSD')
tabcandle = readweekpaire.candelize(letableau)
print(tabcandle)

table=np.zeros(7200)
for i in tabcandle:
   table[i[0]] = i[1]

print (table)

pdtable = pd.DataFrame(table)
length=30
numsd=2.0

ave = pd.stats.moments.rolling_mean(pdtable,length)
sd = pd.stats.moments.rolling_std(pdtable,length)
upband = ave + (sd*numsd)
dnband = ave - (sd*numsd)

print(np.round(ave,3), np.round(upband,3), np.round(dnband,3))

# Plot two charts to assess trades and equity curve
fig = plt.figure()
fig.patch.set_facecolor('white')  # Set the outer colour to white
ax1 = fig.add_subplot(211, ylabel='Price in $')

# Plot the "buy" trades against AAPL
ax1.plot(upband,'^', markersize=10, color='m')
ax1.plot(upband,'^', markersize=10, color='m')

candlestick(ax1, table, width=0.6)
fig.shw()

