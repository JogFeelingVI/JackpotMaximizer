# @Author: JogFeelingVi
# @Date: 2023-03-30 23:06:20
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-12-11 22:35:23

from collections import Counter
import unittest, os, time, itertools, multiprocessing as mp
from codex import glns_v2, rego_v2, Tonji

data = {
    "R": [
        5, 6, 12, 15, 23, 25, 1, 5, 9, 15, 18, 26, 1, 9, 10, 13, 21, 28, 5, 6,
        13, 24, 25, 29, 10, 19, 23, 25, 30, 31, 1, 3, 5, 26, 30, 32, 7, 9, 10,
        20, 22, 24, 3, 7, 18, 25, 29, 33, 1, 3, 6, 8, 18, 24, 6, 8, 10, 13, 16,
        28, 2, 6, 20, 25, 29, 33, 5, 6, 12, 17, 20, 33, 9, 12, 13, 22, 24, 31,
        1, 2, 13, 18, 25, 27, 7, 9, 15, 16, 17, 26, 2, 7, 16, 21, 26, 27, 2, 8,
        9, 13, 24, 27, 2, 11, 14, 17, 18, 28, 1, 2, 11, 19, 25, 29, 1, 2, 3,
        19, 21, 28, 3, 8, 13, 24, 27, 29, 2, 12, 16, 25, 30, 31, 7, 8, 14, 18,
        20, 30, 10, 13, 15, 22, 29, 32, 2, 3, 17, 18, 25, 30, 11, 14, 15, 27,
        30, 33, 10, 24, 26, 28, 29, 31, 3, 8, 19, 22, 26, 32, 7, 16, 20, 21,
        27, 33, 8, 9, 12, 17, 32, 33
    ],
    "B": [
        4, 4, 10, 15, 12, 16, 7, 14, 9, 13, 16, 9, 4, 3, 9, 16, 12, 8, 4, 15,
        8, 12, 5, 15, 11, 4, 16, 14, 1, 4
    ],
    "date":
    "2023-11-12 07:00:33.370573"
}


def chengjie_w():

    glnsv2 = glns_v2.glnsMpls(data)
    rand = glns_v2.random_rb(glns_v2.Range_M(M=33), L=6)
    nLS = [rand.get_number_v2() for x in range(100)]
    f = lambda x: x % 7
    cts = [3, 4, 5, 6]
    for n in nLS:
        s = sorted(n, key=f)
        modg = itertools.groupby(s, key=f)
        counts = [len(list(g[1])) for g in modg]
        ns = map(str, n)
        nct = map(str, counts)
        print(
            f'debug N {" ".join(ns):>17} MOD 7 {":".join(nct):>13} in CTS {counts.__len__() in cts}'
        )


def chengjie_d():
    rand = glns_v2.random_rb(glns_v2.Range_M(M=33), L=6)
    nLS = [rand.get_number_v2() for x in range(50)]
    for n in nLS:
        C = set([x % 10 for x in n])
        sc = ' '.join(map(lambda x: f'{x}', C))
        s = ' '.join(map(lambda x: f'{x:02}', n))
        print(f'n {s:>20} ->> {sc:<11} len {len(C)}')


def frekhz() -> None:
    rangdom_f = glns_v2.random_rb_f(rb=data['R'], L=6)
    rez = [rangdom_f.get_number_v2() for _ in range(100)]
    for re in rez:
        print(f'debug {re}')


def test_change():
    # st = time.time()
    # [chengjie_w() for _ in range(1)]
    # et = time.time()
    # print(f'AC Use Time W {et-st:.4f}')
    st = time.time()
    [chengjie_d() for _ in range(1)]
    et = time.time()
    print(f'AC Use Time D {et-st:.4f}')


def filter_test():
    '''test'''
    glnsv2 = glns_v2.glnsMpls(data)
    filterv2 = glns_v2.filterN_v2()
    filterv2.Last = glnsv2.getlast
    filterv2.Lever = glnsv2.getabc
    filterv2.debug = True
    reego = rego_v2.rego().parse_dict
    tongji = Tonji.tjone()
    tongji.set_tongji_index([4,5,6])
    rand = glns_v2.random_rb(glns_v2.Range_M(M=33), L=6)
    band = glns_v2.random_rb(glns_v2.Range_M(M=16), L=1)
    while len(tongji.nLopp) <= 1000:
        returnd = True
        r = rand.get_number_v2()
        b = band.get_number_v2()
        N = glns_v2.Note(r, b)
        for k, parst in reego.items():
            rex = parst['f'](N, parst['a'])
            if rex == False:
                returnd = False
                break
        for k, func in filterv2.filters.items():
            if func(N) == False:
                returnd = False
                break
        if returnd == True:
            tongji.add(N)
    tongji.echo()


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        #resx = [tesrange() for i in range(1000)]
        filter_test()
        #frekhz()


if __name__ == '__main__':
    unittest.main()
