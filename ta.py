import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt


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

    a = 0.5
    a_ = 1 - a

    for i in xrange(1, lenData):
        y[i] = a*data[i] + a_*y[i - 1]

    return y

def EWMA(data, size): return EMA(data, size)

def main():
    return 0

if __name__ == '__main__':
    main()
