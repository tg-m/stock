import unittest
import numpy as np
import ta

class SMA_Test(unittest.TestCase):
    def test_size_greater_that_data_length_throws_error(self):
        with self.assertRaises(ValueError):
            ta.SMA(np.linspace(1, 1, 1), 22)


    def test_only_ones_in_input_vector(self):
        actual = ta.SMA(np.linspace(1, 1, 10), 3)
        expected = np.linspace(1, 1, 10)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

    def test_arithmethatically_increaing_input(self):
        actual = ta.SMA(np.linspace(1, 10, 10), 3)
        expected = np.concatenate([[1, 4.0/3.0], np.linspace(2, 9, 8)])
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

class CMATest(unittest.TestCase):
    def test_size_greater_than_data_length_throws_errer(self):
        with self.assertRaises(ValueError):
            ta.CMA(np.linspace(1, 1, 1), 2)

    def test_only_ones_in_input_vector(self):
        inData = np.linspace(1, 1, 10)
        actual = ta.CMA(np.linspace(1, 1, 10), 3)
        expected = np.linspace(1, 1, 10)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

    def test_arithmethatically_increaing_input(self):
        actual = ta.CMA(np.linspace(1, 10, 10), 3)
        expected = np.concatenate([[2, 2], np.linspace(2, 5.5, 8)])
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

class WMATest(unittest.TestCase):
    def test_size_greater_than_data_length_throws_errer(self):
        with self.assertRaises(ValueError):
            ta.WMA(np.linspace(1, 1, 1), 2)

    def test_only_ones_in_input_vector(self):
        inData = np.linspace(1, 1, 10)
        actual = ta.WMA(np.linspace(1, 1, 10), 3)
        expected = np.linspace(1, 1, 10)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

    def test_arithmethatically_increaing_input(self):
        actual = ta.WMA(np.linspace(1, 10, 10), 3)
        expected = np.concatenate([[14/6.0, 14/6.0], np.linspace(14, 56, 8)/6.0])
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

class EMATest(unittest.TestCase):
    def test_size_greater_than_data_length_throws_errer(self):
        with self.assertRaises(ValueError):
            ta.EMA(np.linspace(1, 1, 1), 2)

    def test_only_ones_in_input_vector(self):
        inData = np.linspace(1, 1, 10)
        actual = ta.EMA(np.linspace(1, 1, 10), 3)
        expected = np.linspace(1, 1, 10)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

    def test_arithmethatically_increaing_input(self):
        actual = ta.EMA(np.linspace(1, 10, 10), 3)
        expected = np.concatenate([[14/6.0, 14/6.0], np.linspace(14, 56, 8)/6.0])
        return
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))


class MACD_Test(unittest.TestCase):
    def test_MACD_just_call_to_evaluate_correct_implementation(self):
        macd = ta.MACD(np.linspace(1, 5, 50))

class StockData:
    h = np.linspace(4, 4, 10)
    l = np.linspace(0.5, 0.5, 10)
    c = np.linspace(1.5, 1.5, 10)
    o = np.linspace(1.3, 1.5, 10)
    stock = {'low':l, 'high':h, 'close':c, 'open':o}

class TP_Test(unittest.TestCase):
    def test_TP_equal_length_dictionary_as_input(self):
        h = np.linspace(4, 4, 10)
        l = np.linspace(0.5, 0.5, 10)
        c = np.linspace(1.5, 1.5, 10)
        d = {'low':l, 'high':h, 'close':c}
        actual = ta.TP(StockData.stock)
        expected = np.linspace(2, 2, 10)

        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))


class CCI_Test(unittest.TestCase):
    def test_CCI_whether_the_output_has_the_required_length_dictionary_as_input(self):
        actual = ta.CCI(StockData.stock, 4)
        self.failUnless(10 == len(actual))

class DPO_Test(unittest.TestCase):
    def test_DPO_with_even_size(self):
        actual = ta.DPO(StockData.stock, 4)
        self.failUnless(10 == len(actual))

    def test_DPO_with_odd_size(self):
        actual = ta.DPO(StockData.stock, 5)
        self.failUnless(10 == len(actual))

class TR_Test(unittest.TestCase):
    def test_TR_just_call(self):
        actual = ta.TR(StockData.stock)
        self.failUnless(10 == len(actual))

class ATR_Test(unittest.TestCase):
    def test_TR_just_call(self):
        actual = ta.ATR(StockData.stock, 3)
        self.failUnless(10 == len(actual))

class ATRBand_Test(unittest.TestCase):
    def test_TR_just_call(self):
        actual = ta.ATRBand(StockData.stock, 5, 2)
        self.failUnless(10 == len(actual.low))
        self.failUnless(10 == len(actual.high))

class MTM_Test(unittest.TestCase):
    def test_MTM(self):
        actual = ta.MTM(StockData.stock, 1)
        expected = np.concatenate([[1.5], np.linspace(0, 0, 9)])

        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

class RoC_Test(unittest.TestCase):
    def test_RoC(self):
        actual = ta.RoC(StockData.stock, 1)
        expected = np.concatenate([[1.5], np.linspace(1, 1, 9)])

        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

class SRoC_Test(unittest.TestCase):
    def test_SRoC_just_call_and_check_size_of_the_result(self):
        actual = ta.SRoC(StockData.stock, 3, 1)
        self.failUnless(10 == len(actual))

def main():
    unittest.main()


if __name__ == '__main__':
    main()
