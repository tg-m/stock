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


from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

def plotCandlestick(ax, quotes, rWidth=0.3, lWidth=1, colorup='g', colordown='r', alpha=1.0):
    '''
    Plots quotes on the ax axes

    ax        - axes on which plotting takes place
    quotes    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    rWidth    - width of the rectangle
    lWidth    - width of the line
    colorup   - colour used when close >= open
    colordown - colour used when close <  open
    alpha     - the alpha level (recommended is 1.0)

    Note that we plot only quote's dates with NaNs to ensure that x-axis is labeled with
    the proper date format.
    '''
    ax.plot(quotes['date'], np.linspace(np.nan, np.nan, len(quotes)))
    for q in quotes:
        t = q['date']
        o = q['open']
        h = q['high']
        l = q['low']
        c = q['close']

        if c >= o:
            color = colorup
        else:
            color = colordown
        rBottom = min(c, o)
        rHeight = abs(c - o)

        rect = Rectangle(xy = (t, rBottom), width=-rWidth, height=rHeight, facecolor=color, edgecolor=color)
        rect.set_alpha(alpha)
        ax.add_patch(rect)

        rect = Rectangle(xy = (t, rBottom), width=rWidth, height=rHeight, facecolor=color, edgecolor=color)
        rect.set_alpha(alpha)
        ax.add_patch(rect)

        line = Line2D(xdata=(t, t), ydata=(l, h), color=color, linewidth=lWidth, antialiased=True);
        line.set_alpha(alpha)
        ax.add_line(line)

    ax.autoscale_view()

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
        ax.plot(x[x > date], y[x > date], label=label)


    def pltCandle(ax, x, quote, date):
        ta.plotCandlestick(ax, quote[x > date])

    pltCandle(axL, x, d, date)
    #mPlot(axL, x, y, stock.name[0], date)



    for s in [15, 30, 45]:
        mPlot(axL, x, ta.EMA(y, s), ''.join(['EMA ', str(s)]), date)

    #mPlot(axL, x, ta.TP(d), 'TP', date)

    atrb = ta.ATRBand(d, 21, 3)
    mPlot(axL, x, atrb.low, 'ATRB low', date)
    mPlot(axL, x, atrb.high, 'ATRB high', date)

    #axL.plot(x, y, label=stock.name[0])

    #axL.plot(x, ta.TP(d), label='TP')





    for a in actions:
        act_date = dt.datetime.strptime(str(a.date), '%Y-%m-%d').date()
        if act_date >= date:
            axL.text(a.date, d[d['date'] == act_date]['close'], a.action,
                color='red' if a.action.lower() == 'sell' else 'green')


    axL.grid(True)
    axL.legend().draggable()


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

    mPlot(axS, x, roc, 'RoC 1', date)

    #for i in [1, 2, 4, 8]:
        #mPlot(axS, x, ta.MTM(d, i), 'MTM'+str(i), date)




    axS.legend().draggable()

    axS.grid(True)

    plt.show()



def main():
    stockFile = sys.argv[1]
    actionsFile = sys.argv[2]
    date = sys.argv[3]
    x(stockFile, actionsFile, date)


if __name__ == "__main__":
    main()
