import unittest
import numpy as np
import gdax
import math

class OP_Test(unittest.TestCase):
    def test_init(self):
        expectedPrice = 1000.0
        expectedAmount = 2.0
        expectedFee = 0.25
        actual = gdax.OP(expectedPrice, expectedAmount, expectedFee)


        self.assertAlmostEqual(expectedPrice, actual.price)
        self.assertAlmostEqual(expectedAmount, actual.amount)
        self.assertAlmostEqual(expectedFee, actual.fee)


class gain_Test(unittest.TestCase):
    def test_exec(self):
        ops = [gdax.OP(1000.0, 3, 0.035)]
        gdax.gain(ops)

    def test_without_fee(self):
        ops = [gdax.OP(-8000, 0.1, 0.0), gdax.OP(8100, 0.1, 0)]
        actual = gdax.gain(ops)
        expected = 10
        self.assertAlmostEqual(expected, actual)

    def test_with_fee(self):
        ops = [gdax.OP(-100, 1, 1), gdax.OP(200, 1, 1)]
        actual = gdax.gain(ops)
        expected = 97
        self.assertAlmostEqual(expected, actual)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
