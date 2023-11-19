# @Author: JogFeelingVi
# @Date: 2023-03-30 23:06:20
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-19 22:33:04

import unittest, os


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


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        n = 1000
        cpu = os.cpu_count()
        if cpu == None:
            cpu = 4
        rexs = n // cpu + [1,0][n%cpu==0]
        print(f'N/cpu {rexs} cpu {cpu}')


if __name__ == '__main__':
    unittest.main()