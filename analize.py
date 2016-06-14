# -*- coding: utf-8 -*-
import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt
import matplotlib.gridspec as gridspec

from matplotlib.dates import date2num

from matplotlib import finance as fin

import ta

import matplotlib as mpl

from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

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

    d = stock #[stock.date > date]
    #print 'len(d) =', len(d)
    x = d.date
    y = d.close

    def mPlot(ax, x, y, label, date):
        xf = x[x > date]
        t = np.linspace(1, len(xf), len(xf))
        ax.plot(xf, y[x > date], label=label)

    def pltCandle(ax, x, quote, date):
        ta.plotCandlestick(ax, quote[x > date])



    pltCandle(axL, x, d, date)
    #mPlot(axL, x, y, stock.name[0], date)



    #for s in [15, 30, 45]:
        #mPlot(axL, x, ta.EMA(y, s), ''.join(['EMA ', str(s)]), date)

    #mPlot(axL, x, ta.TP(d), 'TP', date)



    atrb = ta.ATRBand(d, 21, 3)
    #mPlot(axL, x, atrb.low, 'ATRB low', date)
    #mPlot(axL, x, atrb.high, 'ATRB high', date)

    #axL.plot(x, y, label=stock.name[0])

    #axL.plot(x, ta.TP(d), label='TP')

    #axL.xaxis.set_major_formatter(mpl.dates.DateFormatter('%Y-%m-%d'))

    for a in actions:
        act_date = dt.datetime.strptime(str(a.date), '%Y-%m-%d').date()
        if act_date >= date:
            axL.text(a.date, d[d['date'] == act_date]['close'], a.action,
                color='red' if a.action.lower() == 'sell' else 'green')


    axL.grid(True)
    #axL.legend().draggable()


    axS = plt.subplot(gs[2, :])
    macd = ta.MACD(y)
    cci = ta.CCI(d, 14)
    dpo = ta.DPO(d, 7)
    tr = ta.TR(d)
    atr = ta.ATR(d, 8)

    mtm1 = ta.MTM(d, 1)
    mtm2 = ta.MTM(d, 2)
    mtm4 = ta.MTM(d, 8)

    roc = ta.RoC(stock, 1)
    sroc = ta.SRoC(stock, 13, 21)

    wmr = ta.Williams(stock, 2)

    stc = ta.Stochastic(stock, 12, 3)

    rsi = ta.RSI(stock,  7)

    mPlot(axS, x, rsi, 'RSI', date)

    #mPlot(axS, x, stc.K, 'K', date)
    #mPlot(axS, x, stc.D, 'D', date)
    #mPlot(axS, x, stc.DSlow, 'D slow', date)



    #for i in [1, 2, 4, 8]:
        #mPlot(axS, x, ta.MTM(d, i), 'MTM'+str(i), date)



    axS.legend().draggable()

    axS.grid(True)

    xticks = map(lambda(y): str(y), x[x > date])
    #print xticks

    #plt.xticks(np.linspace(0, len(xticks), len(xticks)), xticks)
    plt.show()



def main():
    stockFile = sys.argv[1]
    actionsFile = sys.argv[2]
    date = sys.argv[3]
    x(stockFile, actionsFile, date)


if __name__ == "__main__":
    main()
