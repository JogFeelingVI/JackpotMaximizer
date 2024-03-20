# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-20 08:04:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-20 23:07:03

import dataclasses, itertools as itr, concurrent.futures, re
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


def __diff__(s: sublist, M: List, diff: List):
    '''
    echo numbers
    '''
    diff_info = {0: []}
    # jhr = self.fmjhr
    # jhb = self.fmjhb
    # zipo = multip_v3.ccp(Nr, Nb)
    # 发现错误 终止执行程序
    for _m in M:
        if s != _m:
            dif_r = (set(s.rNumber) & set(_m.rNumber)).__len__()
            dif_b: int = (set(s.bNumber) & set(_m.bNumber)).__len__()
            key = f'^{dif_r}{dif_b}[0-6]'
            difex: str = [x for x in diff if re.match(key, x)][0]
            leve = int(difex[-1])
            if leve > 0:
                if leve not in diff_info.keys():
                    diff_info.update({leve:[_m.id]})
                else:
                    _list = diff_info.get(leve,[])
                    _list.append(_m.id)
                    diff_info.update({leve: _list})
        #print(f'Diff info  -> {Nr} {Nb}')
    return diff_info


def create_task(iTQ):
    _s, _Manager, _diff = iTQ
    diff = __diff__(_s, _Manager, _diff)
    cyn = 0
    for l, ids in diff.items():
        match l:
            case 1:
                cyn = cyn + 5000000 * ids.__len__()
            case 2:
                cyn = cyn + 100000 * ids.__len__()
            case 3:
                cyn = cyn + 3000 * ids.__len__()
            case 4:
                cyn = cyn + 200 * ids.__len__()
            case 5:
                cyn = cyn + 10 * ids.__len__()
            case 6:
                cyn = cyn + 5 * ids.__len__()
    return _s.id, cyn


def initTaskQueue():
    global_vars = globals()
    Manager = global_vars['Manager']
    samples = [x for x in Manager]
    diff_data = re.findall('[0-6]{3}', global_vars['DBASE'])
    return itr.product(samples, [Manager], [diff_data])


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
        for future in concurrent.futures.as_completed(futures):
            # 任务完成后，增加完成计数并打印进度
            completed += 1
            temp = future.result()
            sq3.add_cyns_data(temp[0], temp[1])
            # iStorage.append(temp)
            print(f'\033[K{completed} of the total progress has been completed. Cyn {temp[1]:,}.', end='\r')
        print(f'\033[kCompleted 100%')
    iStorage = sq3.get_smallest_cyns(10)
    sq3.drop_cyns_table()
    sq3.disconnect()
    return iStorage

def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
