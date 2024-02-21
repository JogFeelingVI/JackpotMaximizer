# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-02-21 12:37:31
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-02-21 20:01:23
from collections import Counter
from typing import List
from functools import partial
import pathlib, json, inspect, itertools
from codex import ospath, note

CONF = {}

def parseNote(n:List[int], t:List[int]) -> note.Note:
    return note.Note(n,t)

def mod(n: List, m: int):
    ''' mod ? m = 2 3 4 5 6  group (1, [1,2,3])'''
    f = [x % m for x in n]
    s = sorted(f)
    gby = itertools.groupby(s)
    return [list(v).__len__() for g, v in gby]

def saveDictToJson(name: str, value: dict):
    '''保存dict到json文件'''
    F = pathlib.Path(ospath.findAbsp.file_path(name))
    with F.open('w', encoding='utf-8') as Fopen:
        Fopen.write(json.dumps(value, indent=4))


def loadJsonToDict(name: str):
    '''装载filte配置文件'''
    F = pathlib.Path(ospath.findAbsp.file_path(name))
    with F.open('r', encoding='utf-8') as Fopen:
        dicts = dict(json.loads(Fopen.read()))
        return dicts


def initialization():
    global CONF
    df = loadJsonToDict('DataFrame.json')
    fn = loadJsonToDict('filterN_v3.json')
    counter = Counter(df['R'])
    cold = [n for n, f in counter.most_common() if f < 5.01]
    fn['date'] = df['date']
    fn['Last'] = df['R'][-6::]
    fn['Lever'] = cold
    CONF = fn
    saveDictToJson('filterN_v3.json', CONF)
    
    
def classAttrs():
    global CONF
    fter = []
    check  = []
    for fterItem in CONF["filter"]:
        fter.append(fterItem['name'])
        if fterItem['checked']:
            check.append(fterItem['name'])
    return [fter, check]

def Checkfunc():
    global CONF
    temp =  SyntheticFunction()
    fter = {}
    for fterItem in CONF["filter"]:
        if fterItem['checked']:
            fter[fterItem['name']] = temp[fterItem['name']]
    return fter


def SyntheticFunction():
    global CONF
    funx = {}
    for method in inspect.getmembers(works):
        if inspect.isfunction(method[1]):
            funx.update({method[0]: method[1]})
    for fterItem in CONF["filter"]:
        if fterItem['name'] in funx.keys():
            args = [a.name for a in inspect.signature(funx[fterItem['name']]).parameters.values() if a.name not in ['N','n']]
            match args:
                case ['recommend']:
                    func = partial(funx[fterItem['name']],
                           recommend=fterItem['recommend'])
                case ['recommend', 'Last']:
                    func = partial(funx[fterItem['name']],
                           recommend=fterItem['recommend'], Last=CONF['Last'])
                case ['recommend', 'Lever']:
                    func = partial(funx[fterItem['name']],
                           recommend=fterItem['recommend'], Lever=CONF['Lever'])
            
            funx.update({fterItem['name']: func})
    return funx


class works:

    @staticmethod
    def dzx(N: note.Note, recommend: List[int]) -> bool:
        '''xiao zhong da [2,2,2]'''
        g = [range(i, i + 11) for i in range(0, 33, 11)]
        countofg = map(lambda x: N.setnumber_R.intersection(x).__len__(), g)
        return [False, True][max(countofg) in recommend]

    @staticmethod
    def acvalue(N: note.Note, recommend: List[int]) -> bool:
        '''计算数字复杂程度 默认 P len = 6 这里操造成效率低下'''
        p = itertools.product(N.number[1::], N.number[0:5])
        ac = [1 for a, b in p if a - b > 0.1].__len__() - 1 - len(N.number)
        return [False, True][ac in recommend]

    @staticmethod
    def linma(N: note.Note, recommend: List[int], Last:List[int]) -> bool:
        '''计算邻码'''
        plus_minus = 0
        for n in N.number:
            if n + 1 in Last or n - 1 in Last:
                plus_minus += 1
                if plus_minus not in recommend:
                    return False
        return True

    @staticmethod
    def duplicates(N: note.Note, recommend: List[int], Last:List[int]) -> bool:
        '''计算数组是否有重复项目'''
        duplic = N.setnumber_R & set(Last)
        return [False, True][duplic.__len__() in recommend]

    @staticmethod
    def sixlan(N: note.Note, recommend: List[int]) -> bool:
        '''判断红色区域是否等于 1, 2, 3, 4, 5, 6, 7'''
        xi, da = recommend
        rb = [False, True][xi < sum(N.setnumber_R) < da]
        return rb
    
    @staticmethod
    def lianhao(n: note.Note, recommend: List[int]) -> bool:
        count = []
        for v in n.number:
            if not count or v != count[-1][-1] + 1:
                count.append([])
            count[-1].append(v)
        flgrex = sorted([len(v) for v in count if len(v) > 1])
        flg = 6
        match flgrex:
            case []:
                flg = 0
            case [2]:
                flg = 1
            case [2, 2]:
                flg = 2
            case [3]:
                flg = 3
            case [3, 2]:
                flg = 4
            case [4]:
                flg = 5
            case _:
                flg = 7
        return [False, True][flg in recommend]
    
    @staticmethod
    def mod2(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 2))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def mod3(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 3))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def mod4(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 4))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def mod5(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 5))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def mod6(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 6))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def mod7(n: note.Note, recommend: List[int]) -> bool:
        '''mod 3 not in [[6], [5,1],[3,3]]'''
        counts = max(mod(n.number, 7))
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def dx16(n: note.Note, recommend: List[int]) -> bool:
        '''
        da:xiao 1:5 n > 16.02 is da
        '''
        f = lambda x: x > 16.02
        s = sorted(n.number, key=f)
        modg = itertools.groupby(s, key=f)
        counts = max([len(list(g[1])) for g in modg])
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def zhihe(n: note.Note, recommend: List[int]) -> bool:
        '''
        da:xiao 1:5 n > 16.02 is da
        '''
        f = lambda x: x in (1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
        s = sorted(n.number, key=f)
        modg = itertools.groupby(s, key=f)
        counts = max([len(list(g[1])) for g in modg])
        if counts not in recommend:
            return False
        return True
    
    @staticmethod
    def coldns(n: note.Note, recommend: int, Lever:List[int]) -> bool:
        '''
        这个方法会造成命中率降低弃用
        [(4, 1), (20, 3), (7, 3), (23, 3), (21, 3), (2, 4), (29, 4), (28, 4), (5, 4), (12, 4), (17, 4)]
        '''
        ninc = set(Lever).intersection(n.number).__len__()
        if ninc == 0 or ninc <= recommend:
            return False
        return True
    
    @staticmethod
    def onesixdiff(n: note.Note, recommend: int) -> bool:
        '''1 - 6 diff > 15.06'''
        if abs(n.index(1) - n.index(6)) < recommend:
            return False
        return True
    
