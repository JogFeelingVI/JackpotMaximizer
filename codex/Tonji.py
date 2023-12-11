# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-10 20:02:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-12-11 22:39:02
from ast import List
from typing import Any
from codex import glns_v2, rego_v2


class tjone:

    def __init__(self):
        self.nLopp = []
        self.dLoop = {}
        self.index = []
        
    def set_tongji_index(self, index):
        if isinstance(index, list):
            self.index.extend(index)
        if isinstance(index, int):
            t=[index]
            self.index.extend(t)

    def add(self, N: glns_v2.Note):
        ''''''
        self.nLopp.append(N)
        key = ''.join((f'{N.index(x):02}' for x in self.index))
        vis = self.dLoop.get(key, 0) + 1
        self.dLoop.update({key: vis})

    def echo(self):
        combing = []
        f = lambda x: x[1]
        for k, v in sorted(self.dLoop.items(), key=f):
            if v == 1:
                combing.append(k)
            print(f'TongJi Key {k:>2}  {v}')
        print(f'combin for 1 {" ".join(combing[0:15])}')
