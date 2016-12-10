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

def IRR(payments):
    '''
    payments - stream of payments
    '''

    #roots = np.roots(payments)
    #sortedRoots = sorted(roots, key = lambda x : abs(np.imag(x)))

    # item at the end is only needed to truncated pythons zero dimensional array
    # we also substract 1 (one), cause what is computed is 1 + r
    return np.real(sorted(np.roots(payments), key = lambda x : abs(np.imag(x)))[0]).item() - 1


