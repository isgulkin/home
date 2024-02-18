import unittest
import math
from pairs_of_points import closest_pair_of_points


class ClosestTest(unittest.TestCase):
    def testSinglePair(self):
        self.assertCorrectPair(
            closest_pair_of_points([(1, 1), (2, 2)]),
            (1, 1), (2, 2)
        )

    def testThree(self):
        self.assertCorrectPair(
            closest_pair_of_points([(1, 1), (2, 2), (4, 4)]),
            (1, 1), (2, 2)
        )

    def testClose(self):
        d = 0.0001
        self.assertCorrectPair(
            closest_pair_of_points([(d, 0), (1, 0), (0, 1)]),
            (d, 0), (1, 0)
        )
        self.assertCorrectPair(
            closest_pair_of_points([(0, d), (1, 0), (0, 1)]),
            (0, d), (0, 1)
        )

    def testCenter(self):
        self.assertCorrectPair(
            closest_pair_of_points([(1, 2), (2, 3), (2.5, 3.5), (4, 5)]),
            (2, 3), (2.5, 3.5)
        )

    def testMany(self):
        arr = [(0.5, 0)] + [(i, 0) for i in range(-100000, 100000, 2)]
        self.assertCorrectPair(
            closest_pair_of_points(arr),
            (0, 0), (0.5, 0)
        )

    def testAxisX(self):
        arr = [(0, 0.5)] + [(0, i) for i in range(-100, 100, 2)]
        self.assertCorrectPair(
            closest_pair_of_points(arr),
            (0, 0), (0, 0.5)
        )

    def test8(self):
        d = 0.01
        arr = [(0, 0), (0, 1), (-1, d), (1, d), (-1, 2), (1, -2)]
        self.assertCorrectPair(closest_pair_of_points(arr), (0, 0), (0, 1))

    def testEqual(self):
        arr = [(i, j) for i in range(-10, 10) for j in range(-10, 10)]
        res = closest_pair_of_points(arr)
        p1 = res[1]
        p2 = res[2]
        self.assertEqual(res[0], 1)
        self.assertTrue(p1[0] == p2[0] or p1[1] == p2[1])
        self.assertAlmostEqual(math.hypot(
            p1[0] - p2[0], p1[1] - p2[1]), res[0])

    def assertCorrectPair(self, res, p1, p2):
        '''Asserts that closest_pair_of_points returned
        the right pair in any order and
        the correct distance between points'''
        if res[1] > res[2]:
            res = (res[0], res[2], res[1])
        self.assertEqual(res[1], p1)
        self.assertEqual(res[2], p2)
        self.assertAlmostEqual(res[0], math.hypot(
            p1[0] - p2[0], p1[1] - p2[1]))


if __name__ == '__main__':
    unittest.main()