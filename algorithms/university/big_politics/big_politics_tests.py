import unittest
from big_politics import big_politics


class MessageTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(big_politics([2, 6]), 8)

    def test_2(self):
        self.assertEqual(big_politics([6, 2, 4]), 18)

    def test_3(self):
        self.assertEqual(big_politics([9, 10, 6, 1, 5, 4, 3, 7, 2, 8]), 173)

    def test_4(self):
        self.assertEqual(
            big_politics(
                [7, 6, 9, 3, 5, 2, 7, 4, 4, 4, 3, 5, 10, 4, 9, 6, 1, 10, 6,
                 8]), 475)

    def test_5(self):
        self.assertEqual(
            big_politics([
                51, 67, 39, 11, 1, 99, 45, 70, 85, 34, 16, 89, 95, 56, 52, 1,
                61, 58, 90, 91, 5, 10, 41, 100, 11, 73, 20, 50, 80, 64, 37, 48,
                92, 18, 63, 71, 54, 6, 99, 92, 97, 48, 31, 62, 43, 46, 20, 37,
                68, 63, 9, 25, 57, 77, 87, 91, 38, 58, 66, 40, 83, 65, 44, 16,
                76, 51, 70, 90, 71, 84, 83, 22, 58, 59, 88, 54, 23, 27, 13, 72,
                9, 4, 31, 13, 16, 16, 83, 89, 90, 9, 87, 9, 87, 60, 27, 58, 45,
                48, 4, 78
            ]), 33409)

    def test_6(self):
        self.assertEqual(big_politics([1] * 1000), 9976)

    def test_7(self):
        self.assertEqual(big_politics([1] * 10000), 133616)

    def test_8(self):
        self.assertEqual(big_politics([i for i in range(1, 10000)]), 652216968)

    def test_9(self):
        self.assertEqual(big_politics([i**2 for i in range(1, 10000)]),
                         4228678221175)

    def test_10(self):
        self.assertEqual(big_politics([10**9] * 10000), 133616000000000)


if __name__ == "__main__":
    unittest.main()