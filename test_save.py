# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-13 20:25:19
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-12-14 15:08:41

from collections import Counter
from heapq import nlargest
from token import NL
import unittest, os, time, itertools, multiprocessing as mp, pathlib, re
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


def fromat_str(s: str):
    '''
    [-] 03 06 11 18 22 30 + 04
    '''
    fre = re.compile(
        r'([\[\]\+-]{3})\s([\d]{2})\s([\d]{2})\s([\d]{2})\s([\d]{2})\s([\d]{2})\s([\d]{2})\s\+\s([\d]{2})'
    )
    match = fre.match(s)
    if match != None:
        _, *r, b = match.groups()
        nR = [int(x) for x in r]
        nB = int(b)
        return glns_v2.Note(nR, nB)
    return 'N/A'


def step_two(rs: list, index: list):
    '''第二步'''
    over = []
    for i, line in enumerate(rs):
        tjon = Tonji.tjone()
        tjon.set_tongji_index(index)
        tjon.add(line)
        key = list(tjon.dLoop.keys())[0]
        #print(f'step two {key} {index}')
        for x in rs:
            if x == line:
                continue
            tjon.add(x)
        ov = tjon.dLoop[key]
        if ov > 1.01:
            over.append([ov, line])
    f = lambda x: x[0]
    over = sorted(over, key=f)
    for k, n in over:
        print(f'count {k}, N {n}')
    print(f'step two end over len {over.__len__()}')
    return [n for _,n in over]


def step_one():
    '''test'''
    log = pathlib.Path('save.log')
    if log.exists() == False:
        print(f'Save Log is not Exists')
    read_save = []
    nLidata = []
    with open(log, mode='r') as logr:
        read_save = logr.readlines()
    for line in read_save:
        n = fromat_str(line)
        nLidata.append(n)
    print(f'Note Conversion completed len {nLidata.__len__()}')
    read_save.clear()
    for i, line in enumerate(nLidata):
        tjon = Tonji.tjone()
        tjon.set_tongji_index([2, 3, 4, 5])
        tjon.add(line)
        key = list(tjon.dLoop.keys())[0]
        print(f'Start the first -{i:^5} \\ {key} - Statistics')
        for x in nLidata:
            if x == line:
                continue
            tjon.add(x)
        for k, v in tjon.dLoop.items():
            if v == 2 and key == k:
                print(f'  key {k} VA {v}')
                read_save.append(nLidata[i])
    return read_save


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        #resx = [tesrange() for i in range(1000)]
        rs = step_one()
        rs = step_two(rs=rs, index=[1, 2, 3])
        rs = step_two(rs=rs, index=[4,5,6])


if __name__ == '__main__':
    unittest.main()
