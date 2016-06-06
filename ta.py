import sys
from  matplotlib import mlab
from matplotlib import pyplot as plt
import numpy as np
import math
import datetime as dt


def movingAverage(data, size):
    '''
    data - array with numerical data
    size - length of the moving average
    '''

    lenData = len(data)
    if size > lenData:
        raise ValueError('size must be less or equal size of the data')

    result = np.linspace(0, 0, lenData - size + 1)

    s = 0.0

    for i in xrange(size):
        s += data[i]

    result[0] = s

    for i in xrange(size, lenData):
        s -= data[i - size]
        s += data[i]
        result[i - size + 1] = s

    return result/size



def main():
    return 0

if __name__ == '__main__':
    main()
