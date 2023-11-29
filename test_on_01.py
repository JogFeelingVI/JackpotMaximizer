# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-10-20 16:57:06
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-29 14:56:23

import unittest
from codex import multip_v3 as mpv3


def main():
    print("Hello, World!")
    data = {
        "R": [
            5, 6, 12, 15, 23, 25, 1, 5, 9, 15, 18, 26, 1, 9, 10, 13, 21, 28, 5,
            6, 13, 24, 25, 29, 10, 19, 23, 25, 30, 31, 1, 3, 5, 26, 30, 32, 7,
            9, 10, 20, 22, 24, 3, 7, 18, 25, 29, 33, 1, 3, 6, 8, 18, 24, 6, 8,
            10, 13, 16, 28, 2, 6, 20, 25, 29, 33, 5, 6, 12, 17, 20, 33, 9, 12,
            13, 22, 24, 31, 1, 2, 13, 18, 25, 27, 7, 9, 15, 16, 17, 26, 2, 7,
            16, 21, 26, 27, 2, 8, 9, 13, 24, 27, 2, 11, 14, 17, 18, 28, 1, 2,
            11, 19, 25, 29, 1, 2, 3, 19, 21, 28, 3, 8, 13, 24, 27, 29, 2, 12,
            16, 25, 30, 31, 7, 8, 14, 18, 20, 30, 10, 13, 15, 22, 29, 32, 2, 3,
            17, 18, 25, 30, 11, 14, 15, 27, 30, 33, 10, 24, 26, 28, 29, 31, 3,
            8, 19, 22, 26, 32, 7, 16, 20, 21, 27, 33, 8, 9, 12, 17, 32, 33
        ],
        "B": [
            4, 4, 10, 15, 12, 16, 7, 14, 9, 13, 16, 9, 4, 3, 9, 16, 12, 8, 4,
            15, 8, 12, 5, 15, 11, 4, 16, 14, 1, 4
        ],
        "date":
        "2023-11-12 07:00:33.370573"
    }
    iRx = mpv3.run_works(data=data, n=1000, mcp=True, rego=True)
    for x in iRx:
        index, depr, n, r = x
        print(f'{mpv3.prompt} [{index:>4}] dep: {depr:>4} N {n} + {r}')


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        #resx = [tesrange() for i in range(1000)]
        #tesrange()
        #filter_test()
        #is_uncorrelated()
        #test_change()
        main()


if __name__ == '__main__':
    unittest.main()
