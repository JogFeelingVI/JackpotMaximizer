# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-09-21 21:14:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-02-21 19:19:02
import itertools, random, math
from collections import Counter, deque
from codex import groove, note
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


# class filterN_v2:
#     ''' 对Note进行过滤 '''
#     filters = {}

#     __Lever = set()
#     __Last = [0, 0, 0, 0, 0, 0]
#     __debug = False

#     @property
#     def debug(self) -> bool:
#         return self.__debug

#     @debug.setter
#     def debug(self, value: bool) -> None:
#         self.__debug = value
#         self.__init__filters()

#     @property
#     def Lever(self) -> set[Any]:
#         ''' 出号频率等级 '''
#         return self.__Lever

#     @Lever.setter
#     def Lever(self, value: set[Any]) -> None:
#         self.__Lever = value

#     @property
#     def Last(self) -> List[int]:
#         ''' 最后的出号 '''
#         return self.__Last

#     @Last.setter
#     def Last(self, value: List[int]):
#         self.__Last = value

#     @staticmethod
#     def getchecked():
#         return [
#             'sixlan',
#             'dx16',
#             'zhihe',
#             'acvalue',
#             'mod2',
#             'mod3',
#             'mod4',
#             'mod5',
#             'mod6',
#             'mod7',
#         ]

#     def __init__filters(self) -> None:
#         self.filters = {
#             'sixlan': self.sixlan,
#             'onesixdiff': self.onesixdiff,
#             'dx16': self.dx16,
#             'zhihe': self.zhihe,
#             'duplicates': self.duplicates,
#             'linma': self.linma,
#             'dzx': self.dzx,
#             'lianhao': self.lianhao,
#             'acvalue': self.acvalue,
#             'mod2': self.mod2,
#             'mod3': self.mod3,
#             'mod4': self.mod4,
#             'mod5': self.mod5,
#             'mod6': self.mod6,
#             'mod7': self.mod7,
#             'coldns': self.coldns,
#         }

#         if self.__debug == False:
#             #diskey = ['sixlan', 'denji']
#             diskey = [
#                 #'sixlan',
#                 #'duplicates',
#                 #'denji',
#             ]
#             for k in diskey:
#                 self.filters.pop(k)

#     def __init__(self) -> None:
#         self.__init__filters()

#     def dzx(self, N: note.Note) -> bool:
#         '''xiao zhong da [2,2,2]'''
#         g = [range(i, i + 11) for i in range(0, 33, 11)]
#         countofg = map(lambda x: N.setnumber_R.intersection(x).__len__(), g)
#         return [False, True][5 not in countofg or 6 in countofg]

#     def acvalue(self, N: note.Note) -> bool:
#         '''计算数字复杂程度 默认 P len = 6 这里操造成效率低下'''
#         p = itertools.product(N.number[1::], N.number[0:5])
#         ac = [1 for a, b in p if a - b > 0.1].__len__() - 1 - len(N.number)
#         return [False, True][ac >= 4]

#     def linma(self, N: note.Note) -> bool:
#         '''计算邻码'''
#         plus_minus = 0
#         for n in N.number:
#             if n + 1 in self.Last or n - 1 in self.Last:
#                 plus_minus += 1
#                 if plus_minus > 3.5:
#                     return False
#         return True

#     def duplicates(self, N: note.Note) -> bool:
#         '''计算数组是否有重复项目'''
#         duplic = N.setnumber_R & set(self.Last)
#         return [False, True][duplic.__len__() in (0, 1, 2)]

#     def sixlan(self, N: note.Note) -> bool:
#         '''判断红色区域是否等于 1, 2, 3, 4, 5, 6, 7'''
#         rb = [False, True][max(N.setnumber_R) != 6]
#         return rb

#     def lianhao(self, n: note.Note) -> bool:
#         count = []
#         for v in n.number:
#             if not count or v != count[-1][-1] + 1:
#                 count.append([])
#             count[-1].append(v)
#         flgrex = sorted([len(v) for v in count if len(v) > 1])
#         rebool = [False, True][flgrex in [[], [3], [2], [2, 2]]]
#         return rebool

#     def mod3(self, n: note.Note) -> bool:
#         '''mod 3 not in [[6], [5,1],[3,3]]'''
#         cts = [[6], [5, 1]]
#         counts = sorted(mod(n.number, 3))
#         if counts in cts:
#             return False
#         return True

#     def mod4(self, n: note.Note) -> bool:
#         counts = mod(n.number, 4)
#         if max(counts) > 4.01:
#             return False
#         return True

#     def mod2(self, n: note.Note) -> bool:
#         '''mod 2 not in [[6], [5,1],[3,3]]'''
#         cts = [[6], [5, 1]]
#         counts = sorted(mod(n.number, 2))
#         if counts in cts:
#             return False
#         return True

#     def mod5(self, n: note.Note) -> bool:
#         '''mod 5 not in [[6], [5,1],[3,3]]'''
#         cts = [4, 5, 6]
#         counts = max(mod(n.number, 5))
#         if counts in cts:
#             return False
#         return True

#     def mod6(self, n: note.Note) -> bool:
#         '''mod 5 not in [[6], [5,1],[3,3]]'''
#         cts = [4, 5, 3]
#         counts = len(mod(n.number, 6))
#         if counts not in cts:
#             return False
#         return True

#     def mod7(self, n: note.Note) -> bool:
#         '''mod 5 not in [[6], [5,1],[3,3]]'''
#         cts = [4, 5, 3, 6]
#         counts = len(mod(n.number, 7))
#         if counts not in cts:
#             return False
#         return True

#     def dx16(self, n: note.Note) -> bool:
#         '''
#         da:xiao 1:5 n > 16.02 is da
#         '''
#         f = lambda x: x > 16.02
#         cts = [[6], [0]]
#         s = sorted(n.number, key=f)
#         modg = itertools.groupby(s, key=f)
#         counts = sorted([len(list(g[1])) for g in modg])
#         if counts in cts:
#             return False
#         return True

#     def zhihe(self, n: note.Note) -> bool:
#         '''
#         da:xiao 1:5 n > 16.02 is da
#         '''
#         f = lambda x: x in (1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
#         cts = [[6], [0]]
#         s = sorted(n.number, key=f)
#         modg = itertools.groupby(s, key=f)
#         counts = sorted([len(list(g[1])) for g in modg])
#         if counts in cts:
#             return False
#         return True

#     def coldns(self, n: note.Note) -> bool:
#         '''
#         这个方法会造成命中率降低弃用
#         [(4, 1), (20, 3), (7, 3), (23, 3), (21, 3), (2, 4), (29, 4), (28, 4), (5, 4), (12, 4), (17, 4)]
#         '''
#         ninc = self.Lever.intersection(n.number).__len__()
#         if ninc == 0 or 5.0 < ninc <= 2.9:
#             return False
#         return True

#     def onesixdiff(self, n: note.Note) -> bool:
#         '''1 - 6 diff > 15.06'''
#         if abs(n.index(1) - n.index(6)) < 15.09:
#             return False
#         return True


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
                    case 'g':
                        js_data = groove.bitx_read()

                        if js_data != None:
                            r = partial(
                                groove.random_ex(json_data=js_data,
                                                 max_length=self.rLen,
                                                 RBC=groove.RC).creation)
                            b = partial(
                                groove.random_ex(json_data=js_data,
                                                 max_length=self.bLen,
                                                 RBC=groove.BC).creation)
                            self.producer.update({'r': r})
                            self.producer.update({'b': b})
                            print('[g] use Groove')
                        else:
                            print(f'js data is None')

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
