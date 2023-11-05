# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-09-21 21:14:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-10-31 05:48:28

from collections import Counter, deque
import itertools
import random
from typing import List


class Note:

    def __init__(self, n: List[int], T: List[int] | int) -> None:
        """Note

        Args:
            n (List[int]): 1-33 红色号码球
            T (List[int] | int): 1-16 蓝色号码球
        """
        self.number = sorted(n)
        self.tiebie = [T, [T]][isinstance(T, int)]
        if self.number.__len__() < 6 or self.tiebie.__len__() == 0:
            raise Exception(f'Note Creation failed {self.number}')

    def filter(self, func) -> None:
        '''
        filter jiekou
        '''
        self.number = list(filter(func, self.number))

    @property
    def setnumber_R(self):
        return set(self.number)

    @property
    def setnumber_B(self):
        return set(self.tiebie)

    def __str__(self) -> str:
        n = ' '.join([f'{num:02d}' for num in self.number])
        t = ' '.join([f'{num:02d}' for num in self.tiebie])
        return f'{n} + {t}'


class filterN_v2:
    ''' 对Note进行过滤 '''
    filters = {}
    fixrb = {}

    __Lever = {}
    __Last = [0, 0, 0, 0, 0, 0]
    __debug = False
    
    @property
    def debug(self) -> bool:
        return self.__debug
    
    @debug.setter
    def debug(self, value:bool) -> None:
        self.__debug = value

    @property
    def Lever(self) -> dict:
        ''' 出号频率等级 '''
        return self.__Lever

    @Lever.setter
    def Lever(self, value: dict) -> None:
        self.__Lever = value

    @property
    def Last(self) -> List[int]:
        ''' 最后的出号 '''
        return self.__Last

    @Last.setter
    def Last(self, value: List[int]):
        self.__Last = value

    def __init__(self) -> None:
        self.filters = {
            'sixlan': self.sixlan,
            'linma': self.linma,
            'duplicates': self.duplicates,
            'lianhao': self.lianhao,
            'denji': self.denji,
            'hisdiff': self.hisdiff,
            'ac': self.acvalue,
            'dzx': self.dzx
        }
        if self.debug == False:
            diskey = ['sixlan', 'duplicates', 'denji', 'hisdiff']
            for k in diskey:
                self.filters.pop(k)

    def dzx(self, N: Note) -> bool:
        '''xiao zhong da'''
        a = range(1, 34)
        g = [a[i:i + 11] for i in range(0, len(a), 11)]
        count = [[], [], []]
        for ai in N.setnumber_R:
            index = 1
            while True:
                if ai in g[index]:
                    count[index].append(ai)
                    break
                else:
                    if ai < min(g[index]):
                        index -= 1
                    if ai > max(g[index]):
                        index += 1

        flgrex = [len(x) for x in count]
        rebool = [False, True][5 not in flgrex or 6 in flgrex]
        return rebool

    def acvalue(self, N: Note) -> bool:
        '''计算数字复杂程度 默认 P len = 6 这里操造成效率低下'''
        p = list(N.setnumber_R)
        ac = len(set(x - y for x in p[1::] for y in p[0:5] if x > y)) - (len(p) - 1)
        return [False, True][ac >= 4]

    def linma(self, N: Note) -> bool:
        '''计算临码'''
        plus_minus = []
        for n in N.setnumber_R:
            if n + 1 in self.Last or n - 1 in self.Last:
                plus_minus.append(n)
        return [False, True][plus_minus.__len__() in (0, 1, 2, 3)]

    def duplicates(self, N: Note) -> bool:
        '''计算数组是否有重复项目'''
        duplic = N.setnumber_R & set(self.Last)
        return [False, True][duplic.__len__() in (0, 1, 2)]

    def sixlan(self, N: Note) -> bool:
        '''判断红色区域是否等于 1, 2, 3, 4, 5, 6, 7'''
        ntoe = {1, 2, 3, 4, 5, 6}
        rb = [False, True][N.setnumber_R != ntoe]
        return rb

    def lianhao(self, n: Note) -> bool:
        count = []
        for v in n.setnumber_R:
            if not count or v != count[-1][-1] + 1:
                count.append([])
            count[-1].append(v)
        flgrex = sorted([len(v) for v in count if len(v) > 1])
        rebool = [False, True][flgrex in [[], [3], [2], [2, 2]]]
        return rebool

    def hisdiff(self, N: Note) -> bool:
        '''
        hisdiff 与上一期号码对比
        '''
        diff = [abs(a - b) for a, b in itertools.product(N.number, self.Last)]
        Rex = [False, True][diff.count(1) in [0, 1, 2]]
        return Rex

    def denji(self, N: Note) -> bool:
        '''
        [(4, 1), (20, 3), (7, 3), (23, 3), (21, 3), (2, 4), (29, 4), (28, 4), (5, 4), (12, 4), (17, 4)]
        '''
        bools = False
        if self.Lever.keys() == 0:
            return True
        rex = []
        for _, v in self.Lever.items():
            vz = [x[0] for x in v]
            rex.append(any(x in N.setnumber_R for x in vz))
        bools = [False, True][False not in rex]
        return bools


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

    def addNote(self, n: Note) -> int:
        try:
            self.DuLie.append(n)
            return self.DuLie.__len__()
        except:
            return -1


class random_rb:
    '''random R & B'''
    __usew = False

    def __init__(self, rb: List[int], L: int) -> None:
        self.dep = [0] * L
        self.len = L
        self.duilie = rb
        self.nPool = []
        self.weights = None

    @property
    def usew(self) -> bool:
        return self.__usew

    @usew.setter
    def usew(self, value: bool):
        self.__usew = value

    def remark(self):
        self.dep = [0] * self.len

    def find_zero(self) -> int:
        '''find zero'''
        if 0 in self.dep:
            return self.dep.index(0)
        return -1

    def __initializations(self):
        '''initialization data'''
        if self.nPool == [] or self.weights == None:
            counter = Counter(self.duilie)
            total = max(counter.values())
            inverse_freq = {k: total - v for k, v in counter.items()}
            self.nPool = list(inverse_freq.keys())
            self.weights = list(inverse_freq.values())

    def get_number(self):
        find = self.find_zero()
        if find == -1:
            return True

        if self.nPool == []:
            self.__initializations()
        if self.usew:
            result = random.choices(self.nPool, weights=self.weights, k=7)
        else:
            result = random.choices(self.nPool, k=7)
        for num in result:
            if self.__isok(n=num, index=find):
                self.dep[find] = num
                if self.get_number():
                    return True
                self.dep[find] = 0
        return False

    def __isok(self, n: int, index: int) -> bool:
        '''判断数字是否符合标准'''
        if n in self.dep:
            return False
        return True


class glnsMpls:
    '''glns mpls'''

    _rlen = 6
    _blen = 1

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
    def getabc(self) -> dict:
        '''get {I...II...III}'''
        counter = Counter(self.R)
        counter_list = list(counter.items())
        # 按频率对列表进行排序
        counter_list.sort(key=lambda x: x[1])
        # 计算每个等级的元素数量
        level_size = len(counter_list) // 3
        # 将列表分成三个等级
        level1 = counter_list[:level_size]
        level2 = counter_list[level_size:level_size * 2]
        level3 = counter_list[level_size * 2:]
        return {'I': level1, 'II': level2, 'III': level3}

    def __init__(self, cdic: dict) -> None:
        if 'R' in cdic and 'B' in cdic:
            self.R = cdic.get('R', [])
            self.B = cdic.get('B', [])
            if self.R != None and self.B != None:
                self.groupby = [
                    self.R[i:i + 6] for i in range(0, len(self.R), 6)
                ]
                self.FixR = self.__fixrb(max=33, n=self.R)
                self.FixB = self.__fixrb(max=16, n=self.B)

    @staticmethod
    def __fixrb(max: int = 16, n: List[int] = []) -> List[int]:
        '''
        修复 R B 中缺失的数字
        '''
        max_set = set([x for x in range(1, max + 1)])
        if max == 16 or max == 33 and n is not None:
            fix = max_set.difference(set(n))
            if fix is None:
                return list(max_set)
            else:
                n.extend(list(fix))
                return n
        else:
            return list(max_set)

    def creativity(self) -> Note:
        '''产生号码'''
        get_r = random_rb(self.FixR, self.rLen)
        get_b = random_rb(self.FixB, self.bLen)
        while True:
            get_r.get_number()
            get_b.get_number()
            #n = Note(n=get_r.dep, T=get_b.dep)
            if self.maxjac(N=get_r.dep) < 0.24:
                return Note(n=get_r.dep, T=get_b.dep)
            else:
                get_r.remark()
                get_b.remark()

    def maxjac(self, N: List) -> float:
        # [2, 6, 20, 25, 29, 33]
        def jaccard(A: List, B: List) -> float:
            '''相似度 雅卡尔指数'''
            set_a = set(A)
            set_b = set(B)
            intersection = len(set_a.intersection(set_b))
            union = len(set_a.union(set_b))
            return intersection / union
        g = [jaccard(x, N) for x in self.groupby]
        return max(g)
