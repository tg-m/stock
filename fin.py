'''
Finance tools in Python.
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


def SI(PV, r, n, m=1):
    '''
    SI - Simple Interest

    PV - Present Value
    r  - interest rate
    n  - number of periods
    m  - number of capitalisations per each period
    '''
    return PV*r*n


def CI(PV, r, n, m = 1.0):
    '''
    CI - Compount Interest

    PV - Present Value
    r  - interest rate
    n  - number of periods
    m  - number of capitalisations per each period
    '''
    return PV*(math.pow(1.0 + r/m, n*m) - 1.0)

def EI(PV, r, n, m = float('Inf')):
    '''Exponential Interest'''
    return PV*(math.exp(r*n) - 1)

def FV(PV, r, n, m = 1, XI = CI):
    '''
    FV - Future Value

    PV - Present Value
    r  - interest rate
    n  - number of capitalisation periods
    m  - capitalisations per each period
    XI - interest rate mehod: SI, CI, EI
    '''
    return PV + XI(PV, r, n, m)

def PV(FV, r, n, m = 1, XI = CI):
    '''
    PV - Present Value

    FV - Future Value
    r  - interest rate
    n  - number of capitalisation periods
    m  - capitalisations per each period
    XI - interest rate mehod: SI, CI, EI
    '''
    return FV/(1 + XI(1, r, n, m))

def NPV(payments, r):
    '''
    NPV - Net Present Value

    payments - a stream of payments
    r        - return rate
    '''

    result = 0.0

    for i in xrange(len(payments)):
        result = result + payments[i]*math.pow(1 + r, -i)

    return result


def IRR(payments):
    '''
    IRR - Internal Return Rate

    payments - a stream of payments
    '''

    #roots = np.roots(payments)
    #sortedRoots = sorted(roots, key = lambda x : abs(np.imag(x)))

    # item at the end is only needed to truncated pythons zero dimensional array
    # we also substract 1 (one), cause what is computed is 1 + r
    return np.real(sorted(np.roots(payments), key = lambda x : abs(np.imag(x)))[0]).item() - 1


def PI(payments, r, moneyCost = None):
    '''
    MIRR - Modified Internal Return Rate

    payments     - a stream of payments
    r            - discount rate (?)
    moneyCost    - if money cost is different than 'r' it can be directly specified
    '''
    if None == moneyCost:
        moneyCost = r


    pos = 0.0
    neg = 0.0

    for i in xrange(len(payments)):
        if 0 < payments[i]:
            pos = pos + payments[i]*math.pow(1 + r, -i)
        else:
            neg = neg + payments[i]*math.pow(1 + moneyCost, -i)


    return pos/abs(neg)


def MIRR(payments, r, moneyCost=None):
    '''
    MIRR - Modified Internal Return Rate

    payments     - a stream of payments
    r            - reinvestment rate
    moneyCost    - if money cost is different than 'r' it can be directly specified
    '''

    n = len(payments) - 1
    pi = PI(payments, r, moneyCost)

    return (1 + r)*math.pow(pi, 1.0/float(n)) - 1

def Duration(payments):
    '''
    Average duration of investment a.k.a. Macaulay Duration

    payments  - stream of payments (note that Duration can be computed
                only if the first payment is negative and rest is
                positive, otherwise an exception is thrown).
    '''
    times = [x for x in xrange(len(payments))]



    if 0 <= payments[0]:
        raise ValueError("First payment is an investment and should be negativei!")


    for i in xrange(1, len(times)):
        if 0 > payments[i]:
            raise ValueError("Payments should be non-negative for every indexes higher than 0!")

    r = IRR(payments)


    Dsum = 0.0

    for i in xrange(1, len(times)):
        Dsum = Dsum + times[i]*payments[i]*math.pow(1 + r, -times[i])

    return -Dsum / payments[0]

def PaybackPeriod(payments, r):
    '''
    Time after which the initial investment is returned by the discounted payments.

    payments  - stream of payments (note that Duration can be computed
                only if the first payment is negative and rest is
                positive, otherwise an exception is thrown).
    r         - discount/investment rate
    '''

    if 0 <= payments[0]:
        raise ValueError("First payment is an investment and should be negativei!")


    for i in xrange(1, len(payments)):
        if 0 > payments[i]:
            raise ValueError("Payments should be non-negative for every indexes higher than 0!")

    p0 = -payments[0]

    T = 0
    P = 0.0
    d = 0.0

    for i in xrange(1, len(payments)):
        d = payments[i]*math.pow(1 + r, -i)
        if p0 <= P + d:
            break
        else:
            P = P + d
            T = T + 1




    return T + (p0 - P)/d
