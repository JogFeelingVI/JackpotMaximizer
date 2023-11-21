# @Author: JogFeelingVi
# @Date: 2023-03-30 23:06:20
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-21 13:05:05

import unittest, os, time
from codex import glns_v2


def is_uncorrelated(a, b):
    '''计算数字相关度'''
    n = len(a)
    avg_a = (sum(a) / n)
    avg_b = (sum(b) / n)

    covariance = sum((a[i] - avg_a) * (b[i] - avg_b) for i in range(n))
    std_dev_a = ((sum([(x - avg_a)**2 for x in a]) / n))**0.5
    std_dev_b = ((sum([(x - avg_b)**2 for x in b]) / n))**0.5

    pearson_corr = covariance / (n * std_dev_a * std_dev_b)
    return abs(pearson_corr) < 0.4


def Lianhao(nul: list):
    snul = set(nul)
    C = [0] * len(nul)
    for i in range(len(nul) - 1):
        _n = nul[i]
        if {_n + 1, _n - 1} & snul:
            C[i] = 1
    rebool = [False, True][C.count(1) < 4]
    print(f'count {C} {C.count(1)}')
    return rebool


def filter_test():
    '''test'''
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
    glnsv2 = glns_v2.glnsMpls(data)
    filterv2 = glns_v2.filterN_v2()
    filterv2.Last = glnsv2.getlast
    filterv2.Lever = glnsv2.getabc
    filterv2.debug = True
    N = glns_v2.Note(n=[6, 9, 19, 28, 30, 31], T=[6])
    for k, funv in filterv2.filters.items():
        stime = time.time()
        rexf = set([funv(N) for i in range(1000)])
        etime = time.time()
        print(f'filterv2 {k:>10} time {etime-stime:.4f}`s N {N} rexf {rexf}')


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        filter_test()


if __name__ == '__main__':
    unittest.main()
