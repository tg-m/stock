'''
Technical Analysis tools in Python.
'''

from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt

import matplotlib as mpl
from matplotlib import dates

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
    ax.plot(quotes['date'], np.linspace(np.nan, np.nan, len(quotes['date'])), color='k')
    #index = 0
    for q in quotes:
        t = q['date']
        #t = index; index += 1
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



    #labels = [str(d) for d in quotes['date']]
    #lenL = len(labels)
    #loc = mpl.ticker.MultipleLocator(base = lenL/5)
    #loc = mpl.ticker.MaxNLocator(nbins = 7)
    #plt.xticks(np.linspace(1, lenL, lenL), quotes['date'])
    #ax.xaxis.set_major_locator(loc)


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

    returns EWMA(data, size, 2.0/(1.0 + size))
    '''
    return EWMA(data, size, 2.0/(1.0 + size))

def SMMA(data, size):
    '''
    SMMA - Smoothed Modified Moving Average

    data - array with numerical data
    size - length of the moving average

    returns EWMA(data, size, 1.0/size)
    '''
    return EWMA(data, size, 1.0/size)


def EWMA(data, size, alpha):
    '''
    EMA - Exponential Weighted Moving Average

    data - array with numerical data
    size - length of the moving average
    alpha - the exponential degree of weighting decrease

    Note that this function differs from EMA by the fact that the alpha parameter is
    explicitly required. This is also the most generalised version of exponential
    moving average.
    '''

    lenData = len(data)
    if size > lenData: raise ValueError('size must be less or equal the size of the data')

    y = np.linspace(0, 0, lenData)

    y[0] = data[0]

    a = alpha
    a_ = 1 - a

    # TODO:
    # add stopping after number of terms indicating 99.9% of the weights

    for i in xrange(1, lenData):
        y[i] = a*data[i] + a_*y[i - 1]


    return y

class MACDResult(object):
    '''MACD Result'''
    def __init__(self, slow, fast, macd, signal, histogram):
        self.slow = slow
        self.fast = fast
        self.macd = macd
        self.signal = signal
        self.histogram = histogram

def MACD(data, fast_len=12, slow_len=26, signal_len=9, ave=EMA):
    '''
    Moving Average Convergence/Divergence

    fast_len    - length of the smoothing function of the fast line
    slow_len    - length of the smoothing function of the slow line
    signal_len  - length of the smoothing function of the signal
    ave         - smoothing function
    '''
    slow = ave(data, slow_len)
    fast = ave(data, fast_len)
    macd = fast - slow
    signal = ave(macd, signal_len)
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
    size     - length of the smoothing function
    ave      - smoothing function, default: EMA
    '''
    return ave(TR(quote), size)

class ATRBandResult(object):
    '''ATRBand Result'''
    def __init__(self, low, high, name):
        self.low = low
        self.high = high
        self.name = name

def ATRBand(quote, size, aRange, ave=EMA):
    '''
    Averga True Range Bands

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    size     - length of the smoothing function
    aRange   - factor by which True Range is multiplied to construct bands
    ave      - smoothing function, default: EMA
    '''
    atr = ATR(quote, size, ave)
    return ATRBandResult(quote['close']-aRange*atr,
                         quote['close']+aRange*atr,
            ''.join(['ATRBand ', str(size), ' ', str(aRange)]))


def MTM(quote, n, price='close'):
    '''
    Momentum

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n        - ticks before
    price    - open/high/low/close, default: close
    '''
    d = quote[price]
    d_s = np.concatenate([np.linspace(0, 0, n), d[:len(d) - n]])
    return d - d_s

def RoC(quote, n, price='close'):
    '''
    Rate of Change

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n        - ticks before
    price    - open/high/low/close, default: close
    '''
    d = quote[price]
    d_s = np.concatenate([np.linspace(1., 1., n), d[:len(d) - n]])
    return d/d_s

def SRoC(quote, meanSize, n, ave=EMA, price='close'):
    '''
    Smoothed Rate of Change

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    meanSize - length of the smoothing function
    ave      - smoothing function, default: EMA
    n        - ticks before
    price    - open/high/low/close, default: close
    '''
    return RoC({price : ave(quote[price], meanSize)}, n)

def Williams(quote, n):
    '''
    Williams %R Oscillator

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n        - ticks before that should be taken into account`
    '''
    lenQ = len(quote['close'])
    if n > lenQ: raise ValueError('n can not be greater than number of stock quotes')

    l = np.linspace(np.nan, np.nan, lenQ)
    h = np.linspace(np.nan, np.nan, lenQ)

    for i in xrange(lenQ, 0, -1):
        LOW = max(i-n, 0)
        l[i-1] = min(quote['low'][LOW:i])
        h[i-1] = max(quote['high'][LOW:i])


    ch = quote['close'] - h
    hl = h - l
    hl[hl == 0] = -100.0

    return 100.0*(ch/hl)

class StochasticResult(object):
    '''Stochastic Oscillator Result'''
    def __init__(self, K, D, DSlow):
        self.K = K
        self.D = D
        self.DSlow = DSlow

def Stochastic(quote, n, ave_len, ave=SMA, wantSlow=True):
    '''
    Stochastic Oscillator

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n        - ticks before that shouold be taken into account
    ave_len  - length of the smoothing function
    ave      - smoothing function
    wantSlow - whether to include DSlow signal, default: True, but can be set to False in order
               to speed computations slightly

    Note that it returns StochasticResult(K, D, DSlow) thus it
    '''
    lenQ = len(quote['close'])
    if n > lenQ: raise ValueError('n can not be greater than number of stock quotes')

    l = np.linspace(np.nan, np.nan, lenQ)
    h = np.linspace(np.nan, np.nan, lenQ)

    for i in xrange(lenQ, 0, -1):
        LOW = max(i-n, 0)
        l[i-1] = min(quote['low'][LOW:i])
        h[i-1] = max(quote['high'][LOW:i])


    cl = quote['close'] - l
    hl = h - l
    hl[hl == 0] = 100.0

    K = 100.0*(cl/hl)
    D = ave(K, ave_len)
    DSlow = ave(D, ave_len) if wantSlow else None

    return StochasticResult(K, D, DSlow)

def RSI(quote, n, ave=SMMA, price='close'):
    '''
    Relative Strength Index

    quote    - array of dictionaries or objects that have fields: (date, open, high, low, close)
    n        - ticks before that shouold be taken into account
    ave      - smoothing function, default: SMMA
    price    - open/high/low/close
    '''
    lenQ = len(quote['close'])
    if n > lenQ: raise ValueError('n can not be greater than number of stock quotes')

    up = np.linspace(np.nan, np.nan, lenQ)
    down = np.linspace(np.nan, np.nan, lenQ)

    for i in xrange(lenQ, 0, -1):
        LOW = max(i-n, 0)
        q = quote[price][LOW:i]
        d = q[1:] - q[:-1]
        up[i-1]   = sum(d[d>=0])
        down[i-1] = -sum(d[d<0]) # Yes, minus because sum(...) < 0

    RS = ave(up, n)/ave(down, n)

    return 100.0 - 100.0/(1.0 + RS)

def ADX(quote, ave_len, ave=EMA):
    '''
    '''

    up   =     quote['high'] - np.concatenate([[0], quote['high'][:-1]])
    down = -1*(quote['low']  - np.concatenate([[0], quote['low'][:-1]]))

    # arrays MUST be copied in order to prevent changing up/down during zeroing some elements of mUp/mDown
    DM_PLUS = np.copy(up)
    DM_MINUS = np.copy(down)

    DM_PLUS[~(up > down)] = 0
    DM_PLUS[up < 0] = 0

    DM_MINUS[~(down > up)] = 0
    DM_MINUS[down < 0] = 0


    tr = TR(quote)

    ave_DM_p = ave(DM_PLUS, ave_len)
    ave_DM_m = ave(DM_MINS, ave_len)
    ave_tr = ave(tr, ave_len)

    DI = abs(ave_DM_p - ave_DM_m)
    DX = DI/(ave_DM_p + ave_DM_m)

    adx = 100.0*ave(DX, ave_len)

    return adx

