'''
Gdax tools
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


class OP:
    def __init__(self, price, amount, fee):
        '''
            price - price
            amount - amount
            fee - fee in percents!
        '''
        self.price = float(price)
        self.amount = float(amount)
        self.fee = float(fee)


def gain(ops):
    '''
    ops - list of OP
    '''
    total = 0.0;
    for op in ops:
        #print op.amount, "@", op.price, "(", op.fee, "%)"
        print "{0:7} @ {1:9} ({2:5}%)".format(op.amount, op.price, op.fee)
        #print "price = ", op.price
        #print "amount = ", op.amount
        #print "fee = ", op.fee
        total = total + op.price*(op.amount) - abs(op.price*op.amount)*(op.fee/100.0)
    print "total = ", total
    return total

