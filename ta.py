import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt


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
    ax.plot(quotes['date'], np.linspace(np.nan, np.nan, len(quotes)), color='k')
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


def SMA(data, size):
    '''
    SMA - Simple Moving Average

    data - array with numerical data
    size - length of the moving average
    '''

    lenData = len(data)
    if size > lenData: raise ValueError('size must be less or equal the size of the data')

    result = np.linspace(0, 0, lenData)

    x = np.concatenate([np.linspace(data[0], data[0], size - 1), data])

    s = sum(x[:size])


    result[0] = s

    for i in xrange(size, len(x)):
        s += x[i] - x[i - size]
        result[i - size + 1] = s

    return result/size


def CMA(data, size):
    '''
    CMA - Cumulative Moving Average

    data - array with numerical data
    size - length of the moving average
    '''

    lenData = len(data)
    if size > lenData: raise ValueError('size must be less or equal the size of the data')

    result = np.linspace(0, 0, lenData)

    s = sum(data[:size])/size
    result[0:size] = np.linspace(s, s, size) # sets result first 'size' values to s

    for i in xrange(size, lenData):
        result[i] = (data[i] + i*result[i - 1])/(i + 1.0)

    return result;

def WMA(data, size):
    '''
    WMA - Weighted Moving Average

    data - array with numerical data
    size - length of the moving average
    '''

    lenData = len(data)
    if size > lenData: raise ValueError('size must be less or equal the size of the data')

    y = np.linspace(0, 0, lenData)

    x = reduce(lambda x, y: x + y, map(lambda x, y: x*y, data[:size], np.linspace(1, size, size)))
    y[0:size] = np.linspace(x, x, size)

    T = sum(data[:size])

    for i in xrange(size, lenData):
        y[i] = y[i - 1] + size*data[i] - T
        T = T - data[i - size] + data[i]

    D = 0.5*size*(size + 1)
    return y/D

def EMA(data, size):
    '''
    EMA - Exponential (Weighted) Moving Average

    data - array with numerical data
    size - length of the moving average
    '''

    lenData = len(data)
    if size > lenData: raise ValueError('size must be less or equal the size of the data')

    y = np.linspace(0, 0, lenData)

    y[0] = data[0]

    a = 2.0/(1.0 + size)
    a_ = 1 - a

    # TODO:
    # add stopping after number of terms indicating 99.9% of the weights

    for i in xrange(1, lenData):
        y[i] = a*data[i] + a_*y[i - 1]


    return y

def EWMA(data, size): return EMA(data, size)

class MACDResult(object):
    def __init__(self, slow, fast, macd, signal, histogram):
        self.slow = slow
        self.fast = fast
        self.macd = macd
        self.signal = signal
        self.histogram = histogram

def MACD(data, fast_len=12, slow_len=26, signal_len=9, mov_ave=EMA):
    '''Moving Average Convergence/Divergence'''
    slow = mov_ave(data, slow_len)
    fast = mov_ave(data, fast_len)
    macd = fast - slow
    signal = mov_ave(macd, signal_len)
    histogram = macd - signal
    return MACDResult(slow, fast, macd, signal, histogram)

def TP(quote):
    '''
    Typical Price

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    return (quote['high'] + quote['low'] + quote['close'])/3.0

def CCI(quote, size):
    '''
    Commodity Channel Index

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    tp = TP(quote)
    tp_ave = SMA(tp, size)
    denom = 0.015 * SMA(abs(tp - tp_ave), size)
    result = (tp - tp_ave)/denom
    result[0] = 0
    result[1:size] = np.nan
    return result

def DPO(quote, size):
    '''
    Detrended Price Oscillator

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    sma = SMA(quote['close'], size)
    s = int(size)/2 + 1
    result = quote['close'] - np.concatenate([np.linspace(0, 0, s), sma[:len(sma) - s]])

    return result


def TR(quote):
    '''
    True Range
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    lc = len(quote['close'])
    c_prev = np.concatenate([[0.], quote['close'][:lc-1]])

    h_l = quote['high'] - quote['low']
    h_c_prev = abs(quote['high'] - c_prev)
    l_c_prev = abs(quote['low'] - c_prev)
    return np.amax([h_l, h_c_prev, l_c_prev], axis=0)

def ATR(quote, size, ave=EMA):
    '''
    Average True Range
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    return ave(TR(quote), size)

class ATRBandResult(object):
    def __init__(self, low, high, name):
        self.low = low
        self.high = high
        self.name = name

def ATRBand(quote, size, aRange, ave=EMA):
    '''
    Averga True Range Bands
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    atr = ATR(quote, size, ave)
    return ATRBandResult(quote['close']-aRange*atr,
                         quote['close']+aRange*atr,
            ''.join(['ATRBand ', str(size), ' ', str(aRange)]))


def MTM(quote, n, price='close'):
    '''
    Momentum
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n      - ticks before
    price  = open/high/low/close
    '''
    d = quote[price]
    d_s = np.concatenate([np.linspace(0, 0, n), d[:len(d) - n]])
    return d - d_s

def RoC(quote, n, price='close'):
    '''
    Rate of Change
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    d = quote[price]
    d_s = np.concatenate([np.linspace(1., 1., n), d[:len(d) - n]])
    return d/d_s

def SRoC(quote, meanSize, n, ave=EMA, price='close'):
    '''
    Smoothed Rate of Change
    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    '''
    return RoC({price : ave(quote[price], meanSize)}, n)

def main():
    return 0

if __name__ == '__main__':
    main()

