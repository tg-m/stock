import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt

def printCsvName(csv):
    for n in csv.dtype.names:
        print n

def x(stockFile, actionsFile):
    stock = mlab.csv2rec(stockFile, delimiter=',')
    actions = mlab.csv2rec(actionsFile, delimiter=';')


    print np.unique(stock.isin)


    figSize = (16, 9)
    DPI = 100
    fig = plt.figure(figsize=figSize, dpi=DPI)
    ax = fig.add_subplot(111)

    ax.text(dt.date(2015, 2, 2), 50, 'Test')


    d = stock[stock['data'] > dt.date(2015, 1, 1)]
    x = d['data']
    y = d.kurs_zamkniecia


    plt.plot(x, y)

    for a in actions:
        date = dt.datetime.strptime(str(a.date), '%Y-%m-%d').date()
        ax.text(a.date, d[d['data'] == date].kurs_zamkniecia, a.action,
                color='red' if a.action.lower() == 'sell' else 'green')
        #print a.date, a.action, a.amount, '@', d[d.data == date].kurs_zamkniecia
        #print d[d['data'] == date]


    plt.grid(True)
    plt.show()



def main():
    stockFile = sys.argv[1]
    actionsFile = sys.argv[2]
    x(stockFile, actionsFile)


if __name__ == "__main__":
    main()
