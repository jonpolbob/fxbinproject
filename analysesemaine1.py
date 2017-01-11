

import readweekpaire as rwp
import numpy as np
import matplotlib.finance as fnplot
import matplotlib.pyplot as plt

#essais traitemetn d'une semaine'
def plotcandle(dateochl):
    larray = np.asarray(dateochl)

    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    fnplot.candlestick_ochl(ax1,larray.tolist())
    plt.show()



if __name__ == '__main__':
    letableau = rwp.readweek(5, 2016, 'AUDUSD')
    tabcandle = rwp.candelize(letableau)
    #print(tabcandle)
    plotcandle(tabcandle)


