import unittest
import numpy as np
import fin
import math

class SI_Test(unittest.TestCase):
    def test_SI(self):
        actual = fin.SI(100, 0.10, 1)
        expected = 10.0

        #self.failUnless(expected == actual)
        self.assertAlmostEqual(expected, actual)

class CI_Test(unittest.TestCase):
    def test_CI(self):
        actual = fin.CI(100, 0.10, 2)
        expected = 21.0

        self.assertAlmostEqual(expected, actual)

class EI_Test(unittest.TestCase):
    def test_EI(self):
        actual = fin.EI(100, 0.10, 10)
        expected = 100*(math.e - 1)

        self.assertAlmostEqual(expected, actual)

class FV_Test(unittest.TestCase):
    def test_FV(self):
        actual = fin.FV(100, 0.10, 10)
        expected = 100*math.pow(1.1, 10)

        self.assertAlmostEqual(expected, actual)

class PV_Test(unittest.TestCase):
    def test_PV(self):
        actual = fin.PV(110, 0.10, 1)
        expected = 100.0

        self.assertAlmostEqual(expected, actual)

class IRR_Test(unittest.TestCase):
    @staticmethod
    def referenceIRR(payments):
        sortedRoots = sorted(np.roots(payments), key = lambda x : abs(np.imag(x)))
        return np.real(sortedRoots[0]).item() - 1

    def test_short_payment_stream(self):
        payments = [-500, 300, 300]

        actual = fin.IRR(payments)
        expected = IRR_Test.referenceIRR(payments)

        self.assertAlmostEqual(expected, actual)
    def test_long_payment_stream(self):
        payments = [-2500, 300, 300, -900, 1000, 500, -100, 700, 700, 2300]

        actual = fin.IRR(payments)
        expected = IRR_Test.referenceIRR(payments)

        self.assertAlmostEqual(expected, actual)

class PI_Test(unittest.TestCase):
    def test_PI(self):
        actual = fin.PI([-10, 11], 0.1)
        expected = 1.0

        self.assertAlmostEqual(expected, actual)
    def test_PI_2(self):
        actual = fin.PI([-10, 11, 12.1], 0.1)
        expected = 2.0

        self.assertAlmostEqual(expected, actual)


class NPV_Test(unittest.TestCase):
    def test_NPV(self):
        actual = fin.NPV([-10, 11], 0.1)
        expected = 0.0

        self.assertAlmostEqual(expected, actual)
    def test_NPV_2(self):
        actual = fin.NPV([-10, 11, 12.1], 0.1)
        expected = 10.0

        self.assertAlmostEqual(expected, actual)

class MIRR_Test(unittest.TestCase):
    def test_MIRR(self):
        actual = fin.MIRR([-11, 11], 0.1)
        expected = 0.0

        self.assertAlmostEqual(expected, actual)
    def test_MIRR_2(self):
        actual = fin.MIRR([-10, 11, 12.1], 0.1)
        expected = 1.1*math.sqrt(2.0) - 1

        self.assertAlmostEqual(expected, actual)

class PaybackPeriod_Test(unittest.TestCase):
    def test_PaybackPeriod(self):
        actual = fin.PaybackPeriod([-1000, 550, 605, 700], 0.1)
        expected = 2.0

        self.assertAlmostEqual(expected, actual)
    def test_PaybackPeriod_2(self):
        p = 1.1
        actual = fin.PaybackPeriod([-1000, 500*p, 250*p*p, 500*p*p*p], p - 1)
        expected = 2.5

        self.assertAlmostEqual(expected, actual)




def main():
    unittest.main()


if __name__ == '__main__':
    main()
