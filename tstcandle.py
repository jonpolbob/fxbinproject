#programme pour essayer les candle#en particulier pour comprendre la gestion des
#donnees manquantes


tableau=[[1,1,2,3,10]
         ,[2,2,3,1,6]
    , [25, 3, 7, 2, 6]
    , [26, 6, 8, 1, 4]
    , [27, 4, 4, 3, 5]
         ]

import matplotlib.pyplot as plt
import matplotlib.finance as fin
import numpy as np


larray = np.array(tableau)
lafigure = plt.figure()
ax1 = lafigure.add_subplot(111)
fin.candlestick_ohlc (ax1,larray)

plt.show()