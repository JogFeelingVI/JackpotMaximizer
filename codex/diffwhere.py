# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-20 08:04:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-15 21:12:11

import functools
import json
import os
import pathlib
import random
import dataclasses, itertools as itr, concurrent.futures, re, collections
import time
from typing import Iterable, List
from codex import multip_v4, sq3database
from multiprocessing import Manager, cpu_count

cp = "="
ip = " "


def get_function_name(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        function_name = str(func.__name__).upper()
        # 在这里您可以使用函数名称做任何事情
        print(f'Execution of the " {function_name} " programme.')
        print(f"    args {args} {kwargs}")
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f'Function "{function_name}" ran for {elapsed_time:.4f} seconds')
        return result

    return wrapper


@dataclasses.dataclass
class sublist:
    id: int
    rNumber: list
    bNumber: list


def loadJsonToDict():
    """装载filte配置文件"""
    F = pathlib.Path("./DataFrame.json")
    with F.open("r", encoding="utf-8") as Fopen:
        dicts = dict(json.loads(Fopen.read()))
        return dicts


def ccp(a: Iterable, b: Iterable) -> itr.product:
    """ """
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def parseSublist(item=(1, "01 02 11 15 23 32", "13")):
    id, r, b = item
    try:
        r = [int(x) for x in r.split(" ")]
        b = [int(x) for x in b.split(" ")]
    finally:
        return sublist(id, r, b)


def loadDataBase():
    """装载待分析数据 放入Manager"""
    _temp = []
    with sq3database.Sqlite3Database("my_database.db") as sq3:
        temp = sq3.read_data()
        if temp != None:
            for _t in temp:
                _temp.append(parseSublist(_t))
    return _temp


def randome_n(size: int = 6):
    _temp = []
    _base = [x for x in range(1, 34)]
    random.shuffle(_base)
    return sorted(_base[:size])


def randome_t(size: int = 1):
    _temp = []
    _base = [x for x in range(1, 17)]
    while _temp.__len__() != size:
        _t = random.choice(_base)
        if _t not in _temp:
            _temp.append(_t)
    return sorted(_temp)


def loadGroup():
    """Executing comparison group data generation"""
    print("Executing comparison group data generation.")
    # Retds = []
    # for x in range(10000):
    #     Retds.append(randome_n(6))
    # p = multip_v3
    # p.settingLength(10000)
    # p.useRego(False)
    # p.useFilter(False)
    # p.initPostCall(6, 1, "(.*)")
    # Retds = p.tasks_futures()
    conf = {"n": 10000, "loadins": False, "loadfilter": False}
    p = multip_v4
    p.initialization(conf=conf)
    Retds = p.tasked()
    Retds = [parseSublist(x).rNumber for x in Retds]
    # [[72, '03 05 07 16 27 33', '01']
    return Retds


def nextSample():
    # 设置样本数据 样本数据类型为 sublist
    global_vars = globals()
    if global_vars["samples"] == None:
        global_vars["samples"] = global_vars["Manager"][0]
        return True
    else:
        index = global_vars["Manager"].index(global_vars["samples"])
        print(f"index test {index}")
        if index == global_vars["Manager"].__len__() - 1:
            return False
        if index + 1 < global_vars["Manager"].__len__():
            global_vars["samples"] = global_vars["Manager"][index + 1]
        return True


def initTaskQueue_toList():
    """
    sample 样本组 loadDataBase() result
    comparison loadGroup()
    """
    comparison = loadGroup()  # 10000
    return comparison


def __diff__(s: sublist, seq):
    """
    使用 map() 函数计算差异信息，并进行优化。
    M [[task, count, n, t]]
    """

    # 缓存集合
    s_r_numbers_set = set(s.rNumber)

    def calculate_diff(seq_m):
        # (0, [5, 13, 22, 25, 26, 32], [6])
        # _m = [x for x in seq_m]
        # print(f'calculate_diff {_m}')
        temp_s = s_r_numbers_set.copy()
        temp_s.intersection_update(seq_m)
        return len(temp_s)

    # 使用 map() 函数计算每个元素的差异级别
    diff_levels = map(calculate_diff, seq)

    # 创建一个 Counter 对象来统计差异级别
    diff_info = collections.Counter(diff_levels)
    # print(f'{diff_info = }')
    # diff_info Counter({0: 9147, 6: 628, 5: 100, 4: 7})
    return diff_info


def create_task(sample, comparison, pd):
    temp = []
    pid = os.getpid()
    for s in sample:
        s = parseSublist(s)
        # print(f'create_task {s =}')
        # s =sublist(id=215, rNumber=[2, 4, 7, 15, 28, 32], bNumber=[3])
        diff = __diff__(s, comparison)
        # print(f'{diff =} {s=}')

        cyn = {4: 0, 5: 0}
        match diff:
            case {4: a, 5: b}:
                # print(f'5+0 {diff}')
                cyn = {4: a, 5: b}
            case _:
                pass
        if pid in pd.keys():
            pd[pid] += 1
        else:
            pd[pid] = 1

        sumx = sum(pd.values())
        temp.append([s.id, cyn, s.rNumber, s.bNumber])
        if pd[pid] % 5 == 1:
            print(f"\033[K[P] diffwhere mission completed {sumx}", end="\r")
    return temp


def done_task(future, storage: List):
    flist = future.result()
    for fi in flist:
        id, cyns, n, b = fi
        # print(f'done {cyns}')
        if cyns[4] != 0 and cyns[5] != 0:
            storage.append((id, cyns, n, b))


def tasks_futures_proess_mem(result: list = []):
    """
    cyns.from_id, cyns.cyn, data.r_numbers, data.b_numbers
    """
    iStorage = []

    with Manager() as mem:
        pd = mem.dict(collections.defaultdict(int))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            comparison = initTaskQueue_toList()
            # print(f'{comparison[0]}')
            chunk_size = max(1, result.__len__() // cpu_count())
            chunks = [
                result[i : i + chunk_size]
                for i in range(0, result.__len__(), chunk_size)
            ]

            futures = [
                executor.submit(create_task, i, comparison, pd).add_done_callback(
                    lambda f: done_task(f, iStorage)
                )
                for i in chunks
            ]
    print(f'completed 100% {" "* 60}')
    return iStorage
