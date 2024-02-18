from digits_sum import min_digits_sum
import unittest


class DigitsTest(unittest.TestCase):
    def testZeros(self):
        self.assertEqual(min_digits_sum([0, 0]), 0)

    def testOne(self):
        self.assertEqual(min_digits_sum([0, 1]), 1)

    def testOne2(self):
        self.assertEqual(min_digits_sum([0, 1, 1]), 2)

    def test10(self):
        self.assertEqual(min_digits_sum(list(range(10))), 2468 + 13579)
        self.assertEqual(min_digits_sum(list(range(10))[::-1]), 2468 + 13579)

    def testLongZero(self):
        self.assertEqual(min_digits_sum([0] * 10 ** 6), 0)

    def testNoMod(self):
        arr = [3, 2, 4, 1]
        self.assertEqual(min_digits_sum(arr), 37)
        self.assertEqual(arr, [3, 2, 4, 1])

    def testLongNonZero(self):
        self.assertEqual(str(min_digits_sum([1, 2, 3, 4] * 1000)),
                         '2' * 500 + '4' * 500 + '6' * 500 + '8' * 500)
