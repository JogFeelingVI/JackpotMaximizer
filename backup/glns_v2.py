# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-09-21 21:14:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-17 10:14:25
import itertools, random, math
from collections import Counter, deque
from codex import note
from typing import Any, List
from functools import partial


def mod_old(n: List, m: int):
    ''' mod ? m = 2 3 4 5 6'''
    f = lambda x: x % m
    s = sorted(n, key=f)
    gby = itertools.groupby(s, key=f)

    # sorted([len(list(g[1])) for g in gby])
    return [list(v).__len__() for g, v in gby]


def mod(n: List, m: int):
    ''' mod ? m = 2 3 4 5 6  group (1, [1,2,3])'''
    f = [x % m for x in n]
    s = sorted(f)
    gby = itertools.groupby(s)
    return [list(v).__len__() for g, v in gby]


def Range_M(M: int = 16) -> List:
    '''
    M is 33 or 16
    修复 R B 中缺失的数字
    '''
    max_set = [x for x in range(1, M + 1)]
    return max_set


class formation:
    __dulie: deque
    __maxlen = 15

    @property
    def maxlen(self) -> int:
        return self.__maxlen

    @maxlen.setter
    def maxlen(self, value: int) -> int:
        self.__maxlen = value
        return self.__maxlen

    @property
    def DuLie(self) -> deque:
        return self.__dulie

    def queuestr(self) -> str:
        '''
            gsize group size = 5 
            n gsize * n
            +++++-+++++-+++++-+++++-+++
        '''
        temps = ['+'] * self.maxlen
        temps_group = [
            ''.join(temps[i:i + 5]) for i in range(0, self.maxlen, 5)
        ]
        return '-'.join(temps_group)

    def __init__(self, max: int = 15) -> None:
        '''
        max 设置maxlen = 15
        '''
        self.maxlen = max
        self.__dulie = deque([], maxlen=self.maxlen)

    def addNote(self, n: note.Note) -> int:
        try:
            self.DuLie.append(n)
            return self.DuLie.__len__()
        except:
            return -1


class random_rb_f:
    '''根据频率来随机数列'''

    def __init__(self, rb: List, L: int, debug='') -> None:
        '''
        pass
        debug vvvv
        '''
        self.debug = debug
        self.len = L
        if rb != None:
            self.__init_frequency(rb=rb)

    @staticmethod
    def __fixrb(rb: List[int], debug: str = '') -> List[int]:
        '''
        rb = [1,2,3,4....]
        '''
        sr = Range_M(33) if max(rb) > 16.09 else Range_M(16)
        srb = set(rb)
        sr = set(sr)
        m = sr ^ srb
        if debug.count('v') >= 1:
            print(f'[F] {sr} {m}')
        if m.__len__() != 0:
            return rb + list(m)
        return rb

    def __init_frequency(self, rb: List[int]):
        '''初始化 频率'''
        counter = Counter(self.__fixrb(rb, self.debug))
        self.nPool = list(counter.keys())
        self.weights = list(counter.values())
        if self.debug.count('v') >= 1:
            print(f'[v] nPool {self.nPool}')
            print(f'[v] weights {self.weights}')

    def get_number_v2(self):
        '''get number v2'''
        rext = []
        while set(rext).__len__() != self.len:
            rext = random.choices(self.nPool, weights=self.weights, k=self.len)
        return sorted(rext)


class random_rb:
    '''random R & B'''

    def __init__(self, rb: List, L: int) -> None:
        self.len = L
        self.nPool = rb

    def get_number_v2(self):
        dep = sorted(random.sample(self.nPool, k=self.len))
        return dep


class glnsMpls:
    '''glns mpls'''

    _rlen = 6
    _blen = 1
    producer = {}

    @property
    def rLen(self) -> int:
        return self._rlen

    @rLen.setter
    def rLen(self, value: int) -> None:
        if value >= 6 and value <= 19:
            self._rlen = value

    @property
    def bLen(self) -> int:
        return self._blen

    @bLen.setter
    def bLen(self, value: int) -> None:
        if value >= 1 and value <= 16:
            self._blen = value

    @property
    def getlast(self) -> List[int]:
        return self.R[-6:]

    @property
    def getabc(self):  # -> set[Any]:
        '''get {I...II...III}'''
        counter = Counter(self.R)
        cold = [n for n, f in counter.most_common() if f < 5.01]
        return set(cold)

    def __init__(self, cdic: dict, RL: int, BL: int, w: str = 'c') -> None:
        if 'R' in cdic and 'B' in cdic:
            self.rLen = RL
            self.bLen = BL
            self.R = cdic.get('R', [])
            self.B = cdic.get('B', [])
            if self.R != None and self.B != None:
                self.groupby = [
                    self.R[i:i + 6] for i in range(0, len(self.R), 6)
                ]
                match w:
                    case 's':
                        r = partial(
                            random_rb(Range_M(M=33), self.rLen).get_number_v2)
                        b = partial(
                            random_rb(Range_M(M=16), self.bLen).get_number_v2)
                        self.producer.update({'r': r})
                        self.producer.update({'b': b})
                        print('[s] use sample')
                    case 'c':
                        r = partial(
                            random_rb_f(self.R, self.rLen).get_number_v2)
                        b = partial(
                            random_rb_f(self.B, self.bLen).get_number_v2)
                        self.producer.update({'r': r})
                        self.producer.update({'b': b})
                        print('[c] use choices')
                    

            # print(f'glns init done')

    def creativity(self) -> tuple[list[int], list[int]]:
        '''产生号码'''
        #get_r = random_rb(self.FixR, self.rLen)
        # N = Note()
        use_r = self.producer.get('r', None)
        use_b = self.producer.get('b', None)
        if use_b == use_r == None:
            raise ValueError('[P] producer error')
        return (use_r(), use_b())

    def cosv(self, N: List) -> float:
        dot = sum(a * b for a, b in zip(N, self.getlast))
        normx = math.sqrt(sum([a * a for a in N]))
        normy = math.sqrt(sum([a * a for a in self.getlast]))
        cos = dot / (normx * normy)
        return cos
