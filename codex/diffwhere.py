# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-20 08:04:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-02 22:50:26

import functools
import json
import pathlib
import random
import dataclasses, itertools as itr, concurrent.futures, re, collections
import time
from typing import Iterable, List
from codex import multip_v3, sq3database
from multiprocessing import Manager as __mange



def get_function_name(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        function_name = str(func.__name__).upper()
        # 在这里您可以使用函数名称做任何事情
        print(f'Execution of the " {function_name} " programme.')
        print(f'    args {args} {kwargs}')
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f'Function "{function_name}" ran for {elapsed_time:.4f} seconds')
        return result

    return wrapper

class insrt:

    def __init__(self, code: int, reP: re.Pattern) -> None:
        self.code = code
        self.reP = reP

@dataclasses.dataclass
class sublist:
    id: int
    rNumber: list
    bNumber: list


def loadJsonToDict():
    '''装载filte配置文件'''
    F = pathlib.Path('./DataFrame.json')
    with F.open('r', encoding='utf-8') as Fopen:
        dicts = dict(json.loads(Fopen.read()))
        return dicts

def ccp(a: Iterable, b: Iterable) -> itr.product:
    '''
        '''
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def parseSublist(item=(1, '01 02 11 15 23 32', '13')):
    id, r, b = item
    try:
        r = [int(x) for x in r.split(' ')]
        b = [int(x) for x in b.split(' ')]
    finally:
        return sublist(id, r, b)


def loadDataBase():
    '''装载待分析数据 放入Manager'''
    _temp = []
    with sq3database.Sqlite3Database('my_database.db') as sq3:
        temp = sq3.read_data()
        if temp != None:
            for _t in temp:
                _temp.append(parseSublist(_t))
    return _temp
        

def randome_n(size: int = 6):
    _temp = []
    _base = [x for x in range(1, 34)]
    while _temp.__len__() != size:
        _t = random.choice(_base)
        if _t not in _temp:
            _temp.append(_t)
    return sorted(_temp)

def randome_t(size: int = 1):
    _temp = []
    _base = [x for x in range(1, 17)]
    while _temp.__len__() != size:
        _t = random.choice(_base)
        if _t not in _temp:
            _temp.append(_t)
    return sorted(_temp)

def loadGroup():
    '''Executing comparison group data generation'''
    print('Executing comparison group data generation.')
    p = multip_v3
    p.settingLength(10000)
    p.useRego(False)
    p.initPostCall(loadJsonToDict(), 6, 1,'(.*)','s')
    Retds = p.tasks_futures()
    return Retds

def nextSample():
    # 设置样本数据 样本数据类型为 sublist
    global_vars = globals()
    if global_vars['samples'] == None:
        global_vars['samples'] = global_vars['Manager'][0]
        return True
    else:
        index = global_vars['Manager'].index(global_vars['samples'])
        print(f'index test {index}')
        if index == global_vars['Manager'].__len__() - 1:
            return False
        if index + 1 < global_vars['Manager'].__len__():
            global_vars['samples'] = global_vars['Manager'][index + 1]
        return True
    
def initTaskQueue(result:list=[]):
    if result == []:
        duibizu = loadDataBase()
    else:
        duibizu = result
    wan = loadGroup() #10000
    return itr.product(duibizu, [wan])

def __diff__(s: sublist, seq: List):
        """
        使用 map() 函数计算差异信息，并进行优化。
        M [[task, count, n, t]]
        """

        # 缓存集合
        s_r_numbers_set = set(s.rNumber)

        def calculate_diff(m):
            # (0, [5, 13, 22, 25, 26, 32], [6])
            # print(f'calculate_diff {m=}')
            _, n, _ = m
            if s.rNumber != n:
                dif_r = len(s_r_numbers_set & set(n))
                return dif_r
            return 6

        # 使用 map() 函数计算每个元素的差异级别
        diff_levels = map(calculate_diff, seq)

        # 创建一个 Counter 对象来统计差异级别
        diff_info = collections.Counter(diff_levels)
        # print(f'diff_info {diff_info}')
        # diff_info Counter({0: 9147, 6: 628, 5: 100, 4: 7}) 
        return diff_info
    


def create_task(iQx):
    s, m = iQx
    s = parseSublist(s)
    # print(f'create_task {s =}')
    # s =sublist(id=215, rNumber=[2, 4, 7, 15, 28, 32], bNumber=[3])
    diff = __diff__(s, m)
    # print(f'{type(diff) = }')
    cyn = 0
    # print(f'overlook {diff}')
    # overlook Counter({0: 9225, 6: 571, 5: 81, 4: 5})
    for l, ids in diff.items():
        # print(f'{l=} -> {ids = }')
        match l:
            case 4|5|6:
                # cyn = cyn + 10 * ids
                cyn += ids
            case _:
                pass
    return s.id, cyn, s.rNumber, s.bNumber

def tasks_futures_proess_mem(result:list=[]):
    '''
    cyns.from_id, cyns.cyn, data.r_numbers, data.b_numbers
    '''
    iStorage = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_task, i) for i in initTaskQueue(result=result)]
        completed = 0
        cp = '='
        ip = ' '
        futures_len =futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            # 任务完成后，增加完成计数并打印进度
            completed += 1
            id, cyns , n, b= future.result()
            iStorage.append((id, cyns, n, b))
            bil = completed / futures_len
            # iStorage.append(temp)
            print(f'\033[K[{cp*int(bil*50)}{ip*(50-int(bil*50))}] {bil*100:.2f}%', end='\r')
        print(f'\033[K[ {completed} ] 100%')
    return iStorage

