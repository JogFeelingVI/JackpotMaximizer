# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-26 14:30:53
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-27 16:56:23

import collections
import random, concurrent.futures, itertools
from codex import sq3database
from multiprocessing import Manager
from time import sleep

base = [x for x in range(1, 81)]
count = 0
allsize = 10000


def randome_number(seq, size: int = 10):
    global base
    _temp = []
    _base = base
    while _temp.__len__() != size:
        _t = random.choice(_base)
        if _t not in _temp:
            _temp.append(_t)
    seq.put(sorted(_temp))
    return 1

def writetodata(seq):
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    sq3.create_table()
    sq3.clear_database()
    const = 0
    #sleep(0)
    while seq.empty() == False:
        # sq3.add_data(temp, 'N/a')
        n = seq.get()
        ns = ' '.join((f'{x:02}' for x in n))
        sq3.add_data(ns, 'N/a')
        const += 1   
    sq3.disconnect()
    return const

def put_done(future):
    global count
    global allsize
    cp = '='
    ip = ' '
    
    count += future.result()
    bil = count / allsize
    print(f'\033[K[{cp*int(bil*50)}{ip*(50-int(bil*50))}] {bil*100:.2f}%',
                end='\r')
    return 1

def done(future):
    print(f'\033[K[ {future.result()} ] 100% Done.')
    return 0

def Make_happy_number_8(size:int=10, length:int=10000):
    print(f'Make happy number 8')
    with Manager() as mdict:
        share = mdict.Queue()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(randome_number, share, size).add_done_callback(put_done) for _ in range(length)]
            futures.insert(3, executor.submit(writetodata, share).add_done_callback(done))            
            
    

def initTaskQueue(temp:list):
    samples = [x for x in temp]
    return itertools.product(samples, [temp])

def paresList(s:tuple):
    id, r, Na = s
    r = [int(x) for x in r.split(' ')]
    return (id, r, Na)

def __diff__(s:tuple, M: list, seq):
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
    seq.put(s[0], diff_info)
    return 1


def writetocyns(seq, diff):
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    sq3.create_cyns_table()
    sq3.clear_cyns()
    const = 0
    while seq.empty() == False:
        # sq3.add_data(temp, 'N/a')
        n = seq.get()
        if isinstance(n, list):
            id,  _temp = n
            cyns = 0
            for l, idx in _temp.items():
                if l in diff:
                    cyns += idx
            if cyns >= 1:
                sq3.add_cyns_data(id, cyns)
        const += 1   
    sq3.disconnect()
    return const

def Compare_the_differences(diff:list=[3,4,5,6]):
    # iStorage[0] = (1, '10 11 15 21 32 36 38 55 59 79', 'N/a')
    global allsize
    global count
    count = 0
    print(f'Compare the differences')
    sq3 = sq3database.Sqlite3Database('my_database.db')
    sq3.connect()
    iStorage = sq3.read_data()
    sq3.disconnect()
    if iStorage == None:
        return
    else:
        allsize = iStorage.__len__()
    with Manager() as mdict:
        share = mdict.Queue()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(__diff__, s, M, share).add_done_callback(put_done) for s, M in initTaskQueue(iStorage)]
            futures.insert(3, executor.submit(writetocyns, share, diff).add_done_callback(done))

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
            case 'step_ax':
                global allsize
                size = v['size'] 
                allsize = v['length']
                print(f'{k} args {size=} {allsize=}')
                temp = Make_happy_number_8(size, allsize)
            case 'step_b':
                diff = v['diff']
                print(f'{k} {diff=}')
                Compare_the_differences(diff)

if __name__ == "__main__":
    main()
