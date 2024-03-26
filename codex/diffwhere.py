# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-20 08:04:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-26 14:51:47

import dataclasses, itertools as itr, concurrent.futures, re, collections
from typing import Iterable, List
from codex import sq3database

Manager = []
DBASE = '611602513504414405315216116016000300200100'


@dataclasses.dataclass
class sublist:
    id: int
    rNumber: list
    bNumber: list


def ccp(a: Iterable, b: Iterable) -> itr.product:
    '''
        '''
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def parseSublist(item=(1, '01 02 11 15 23 32', '13')):
    id, r, b = item
    r = [int(x) for x in r.split(' ')]
    b = [int(x) for x in b.split(' ')]
    return sublist(id, r, b)


def loadDataBase():
    with sq3database.Sqlite3Database('my_database.db') as sq3:
        global_vars = globals()
        temp = sq3.read_data()
        if temp != None:
            for _t in temp:
                global_vars['Manager'].append(parseSublist(_t))
            return len(global_vars['Manager'])
        return 0


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


def __diff__(s: sublist, M: List):
        """
        使用 map() 函数计算差异信息，并进行优化。
        """

        # 缓存集合
        s_r_numbers_set = set(s.rNumber)

        def calculate_diff(m):
            if s != m:
                dif_r = len(s_r_numbers_set & set(m.rNumber))
                return dif_r
            return 0

        # 使用 map() 函数计算每个元素的差异级别
        diff_levels = map(calculate_diff, M)

        # 创建一个 Counter 对象来统计差异级别
        diff_info = collections.Counter(diff_levels)
        # print(f'diff_info {diff_info}')
        # diff_info Counter({0: 9147, 6: 628, 5: 100, 4: 7}) 
        return diff_info


def create_task(iTQ):
    _s, _Manager = iTQ
    diff = __diff__(_s, _Manager)
    cyn = 0
    # print(f'overlook {diff}')
    # overlook Counter({0: 9225, 6: 571, 5: 81, 4: 5})
    for l, ids in diff.items():
        # print(f'{l=} -> {ids = }')
        match l:
            case 5:
                # cyn = cyn + 10 * ids
                cyn += ids
            case 6:
                # cyn = cyn + 5 * ids
                cyn += ids
            case _:
                pass
    return _s.id, cyn


def initTaskQueue():
    global_vars = globals()
    Manager = global_vars['Manager']
    samples = [x for x in Manager]
    return itr.product(samples, [Manager])


def tasks_futures():
    with concurrent.futures.ProcessPoolExecutor() as cfp:
        iStorage = []
        results = cfp.map(create_task, initTaskQueue())
        iStorage = sorted(results, key=lambda x: x[1])
        return iStorage

def tasks_futures_proess():
    iStorage = []
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    sq3.create_cyns_table()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_task, i) for i in initTaskQueue()]
        completed = 0
        cp = '='
        ip = ' '
        futures_len =futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            # 任务完成后，增加完成计数并打印进度
            completed += 1
            temp = future.result()
            if 1000 > temp[1] > 0:
                sq3.add_cyns_data(temp[0], temp[1])
            bil = completed / futures_len
            # iStorage.append(temp)
            print(f'\033[K[{cp*int(bil*50)}{ip*(50-int(bil*50))}] {bil*100:.2f}%', end='\r')
        print(f'\033[K[ {completed} ] 100%')
    iStorage = sq3.get_smallest_cyns(15)
    #sq3.drop_cyns_table()
    sq3.disconnect()
    return iStorage

