# @Author: JogFeelingVi
# @Date: 2023-03-30 23:06:20
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-10-19 16:25:34

import unittest

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

def Lianhao(nul:list):
    snul = set(nul)
    C = [0] * len(nul)
    for i in range(len(nul) - 1):
        _n = nul[i]
        if {_n+1, _n-1} & snul:
            C[i] = 1
    rebool = [False, True][C.count(1) < 4]
    print(f'count {C} {C.count(1)}')
    return rebool

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        a = [1, 4, 9, 10, 20, 33]
        c = [1, 4, 19, 21, 25, 33]
        b = [2, 3, 9, 11, 12, 17]
        rexs = Lianhao(a)
        self.assertEqual(rexs, True)

if __name__ == '__main__':
    unittest.main()