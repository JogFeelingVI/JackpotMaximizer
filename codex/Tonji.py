# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-10 20:02:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-12-15 15:57:46
import re
from typing import Any, List, Generator
from codex import glns_v2, rego_v2


class tjone:
    fmts = re.compile(r'([\d]{5})')

    def __init__(self):
        '''
        nLopp 保存原始序列
        dLoop 保存统计序列
        dLpn 保存对应的key序列
        '''
        self.nLopp = []
        self.dLoop = {}
        self.dLpn = {}
        self.keys = [1, 2, 3]

    def set_tongji_index(self, index):
        self.keys.clear()
        if isinstance(index, list):
            self.keys.extend(index)
        if isinstance(index, int):
            t = [index]
            self.keys.extend(t)

    def add(self, N: glns_v2.Note):
        ''''''
        self.nLopp.append(N)
        key = ''.join((f'{N.index(x):02}' for x in self.keys))
        vis = self.dLoop.get(key, 0) + 1
        vin = self.dLpn.get(key, '') + f'{self.nLopp.index(N):05}'
        self.dLoop.update({key: vis})
        self.dLpn.update({key: vin})

    def where_key(self, key) -> Generator[int, None, None] | None:
        '''where is key'''
        indexs = self.dLpn.get(key, '')
        match = self.fmts.findall(indexs)
        if match!=None:
            rx = (int(x) for x in match)
            return rx
        return None

    def echo(self):
        combing = []
        f = lambda x: x[1]
        for k, v in sorted(self.dLoop.items(), key=f):
            if v == 1:
                combing.append(k)
            print(f'TongJi key {k} vount {v}')
        print(f'- {" ".join(combing[0:15])} @combin')
        return combing
