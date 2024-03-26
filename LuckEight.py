# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-26 14:30:53
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-26 16:33:50

import collections
import random, concurrent.futures, itertools
from codex import sq3database

base = [x for x in range(1, 81)]


def randome_number(size: int = 10):
    global base
    _temp = []
    _base = base
    while _temp.__len__() != size:
        _t = random.choice(_base)
        if _t not in _temp:
            _temp.append(_t)
    return sorted(_temp)


def Make_happy_number_8(size:int=10, length:int=10000):
    print(f'Make happy number 8')
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    sq3.create_cyns_table()
    sq3.clear_database()
    cp = '='
    ip = ' '
    iStorage = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(randome_number, size) for _ in range(length)]
        completed = 0
        futures_len = futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            # 任务完成后，增加完成计数并打印进度
            completed += 1 
            temp = future.result()
            # if 1000 > temp[1] > 0:
            temp = ' '.join((f'{x:02}' for x in temp))
            sq3.add_data(temp, 'N/a')
            bil = completed / futures_len
            # 
            print(
                f'\033[K[{cp*int(bil*50)}{ip*(50-int(bil*50))}] {bil*100:.2f}%',
                end='\r')
        print(f'\033[K[ {completed} ] 100%')
    iStorage = sq3.read_data()
    sq3.disconnect()
    return iStorage

def initTaskQueue(temp:list):
    samples = [x for x in temp]
    return itertools.product(samples, [temp])

def paresList(s:tuple):
    id, r, Na = s
    r = [int(x) for x in r.split(' ')]
    return (id, r, Na)

def __diff__(s:tuple, M: list):
    # 缓存集合
    # temp[0] = (1, '07 11 12 15 26 50 62 65 66 75', 'N/a')
    _s = paresList(s)
    s_r_numbers_set = set(_s[1])

    def calculate_diff(m):
        if s != m:
            m = paresList(m)
            dif_r = len(s_r_numbers_set & set(m[1]))
            return dif_r
        return 0

    # 使用 map() 函数计算每个元素的差异级别
    diff_levels = map(calculate_diff, M)

    # 创建一个 Counter 对象来统计差异级别
    diff_info = collections.Counter(diff_levels)
    # print(f'diff_info {diff_info}')
    # diff_info Counter({0: 9147, 6: 628, 5: 100, 4: 7}) 
    return s[0], diff_info

def Compare_the_differences(diff:list=[3,4,5,6]):
    # iStorage[0] = (1, '10 11 15 21 32 36 38 55 59 79', 'N/a')
    print(f'Compare the differences')
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    sq3.create_cyns_table()
    sq3.clear_cyns()
    cp = '='
    ip = ' '
    iStorage = sq3.read_data()
    if iStorage == None:
        return
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(__diff__, s, M) for s, M in initTaskQueue(iStorage)]
        completed = 0
        futures_len = futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            # 任务完成后，增加完成计数并打印进度
            completed += 1 
            id,  _temp = future.result()
            # print(f'{id=} {_temp = }')
            # iStorage.append(temp)
            cyns = 0
            for l, idx in _temp.items():
                if l in diff:
                    cyns += idx
            if cyns >= 1:
                sq3.add_cyns_data(id, cyns)
            #sq3.add_data(temp, 'N/a')
            bil = completed / futures_len
            # 
            print(
                f'\033[K[{cp*int(bil*50)}{ip*(50-int(bil*50))}] {bil*100:.2f}%',
                end='\r')
        print(f'\033[K[ {completed} ] 100%')
    sq3.disconnect()
    return iStorage
        

def main():
    print(f'Hello, World!')
    seting = {
        'step_a': {
            'size': 10,
            'length': 10000
        },
        'step_b': {
            'diff': [8, 9, 10],
        }
    }
    for k, v in seting.items():
        
        match k:
            case 'step_a':
                continue
                size = v['size'] 
                length = v['length']
                print(f'{k} args {size=} {length=}')
                temp = Make_happy_number_8(size, length)
            case 'step_b':
                diff = v['diff']
                print(f'{k} {diff=}')
                Compare_the_differences(diff)

if __name__ == "__main__":
    main()
