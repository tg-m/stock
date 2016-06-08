# -*- coding: utf-8 -*-
import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt
import matplotlib.gridspec as gridspec

import ta


def printCsvName(csv):
    for n in csv.dtype.names:
        print n

def x(stockFile, actionsFile, date):
    stock = mlab.csv2rec(stockFile, delimiter=';')
    actions = mlab.csv2rec(actionsFile, delimiter=';')
    date = dt.datetime.strptime(date, '%Y-%m-%d').date()


    #printCsvName(stock)

    figSize = (16, 9)
    DPI = 100



    fig = plt.figure(figsize=figSize, dpi=DPI)
    gs = gridspec.GridSpec(3, 1)
    axL = plt.subplot(gs[:2, :])

    #axL.text(dt.date(2015, 2, 2), 50, 'Test')

    d = stock[stock.date > date]
    #print 'len(d) =', len(d)
    x = d.date
    y = d.close

    axL.plot(x, y, label=stock.name[0])

    axL.plot(x, ta.EMA(y, 4), label='EMA 4')
    axL.plot(x, ta.EMA(y, 9), label='EMA 9')
    axL.plot(x, ta.EMA(y, 18), label='EMA 18')
    axL.plot(x, ta.EMA(y, 35), label='EMA 35')





    for a in actions:
        act_date = dt.datetime.strptime(str(a.date), '%Y-%m-%d').date()
        if act_date >= date:
            axL.text(a.date, d[d['date'] == act_date].kurs_zamkniecia, a.action,
                color='red' if a.action.lower() == 'sell' else 'green')


    axL.grid(True)
    axL.legend(loc='best')


    axS = plt.subplot(gs[2, :])
    macd = ta.MACD(y)

    axS.plot(x, macd.macd, label='MACD', linewidth=2, color='r')
    axS.plot(x, macd.signal, label='signal', linewidth=1, color='g')
    axS.bar(x, macd.histogram, label='histogram', color='b')

    axS.legend(loc='best')

    axS.grid(True)

    plt.show()



def main():
    stockFile = sys.argv[1]
    actionsFile = sys.argv[2]
    date = sys.argv[3]
    x(stockFile, actionsFile, date)


if __name__ == "__main__":
    main()
