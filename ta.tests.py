import unittest
import numpy as np
import ta

class movingAverageTest(unittest.TestCase):
    def test_size_greater_that_data_length_throws_error(self):
        with self.assertRaises(ValueError):
            ta.movingAverage(np.linspace(1, 1, 1), 22)


    def test_only_ones_in_input_vector(self):
        inData = np.linspace(1, 1, 10)
        actual = ta.movingAverage(inData, 3)
        expected = np.linspace(1, 1, 8)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))

    def test_arithmethatically_increaing_input(self):
        inData = np.linspace(1, 10, 10)
        actual = ta.movingAverage(inData, 3)
        expected = np.linspace(2, 9, 8)
        self.failUnless(len(expected) == len(actual))
        self.failUnless(all(expected == actual))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
