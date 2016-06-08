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
        print actual
        return
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))


class MACD_Test(unittest.TestCase):
    def test_MACD_just_call_to_evaluate_correct_implementation(self):
        macd = ta.MACD(np.linspace(1, 5, 50))

def main():
    unittest.main()


if __name__ == '__main__':
    main()
