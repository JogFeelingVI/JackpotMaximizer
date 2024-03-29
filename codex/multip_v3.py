# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-29 22:17:51
from datetime import datetime as dtime
import json
import re, itertools as itr, concurrent.futures
from typing import List, Iterable
from codex import glns_v2, rego_v3, note, filters_v3, sq3database


bastdata = {'depth': 3000, 'prompt': '[=]', 'rego': False, 'length': 25}
procdata = {}


def ccp(a: Iterable, b: Iterable) -> itr.product:
    '''
        '''
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def useRego(use: bool):
    ''' False rego NO '''
    global_vars = globals()
    global_vars['bastdata']['rego'] = use
    return use


def settingLength(n: int = 25):
    ''' False rego NO '''
    global_vars = globals()
    global_vars['bastdata']['length'] = n
    return n


def initPostCall(cdic: dict, r: int, b: int, iRx: str, scw: str):
    global_vars = globals()
    temp = {}
    fite = filters_v3
    fite.initialization()
    temp['glns'] = glns_v2.glnsMpls(cdic, r, b, scw).producer
    temp['rego'] = rego_v3.Lexer().pares(rego_v3.load_rego_v2())
    temp['filter'] = fite.Checkfunc()
    temp['depth'] = global_vars['bastdata']['depth']
    temp['iRx'] = try_iRx(iRx=iRx)
    global_vars['procdata'] = temp

def try_iRx(iRx:str):
    try:
        _r = re.compile(iRx)
    except:
        _r = re.compile('(.*)')
    finally:
        return _r

def initTaskQueue():
    global_vars = globals()
    length = global_vars['bastdata']['length']
    rego = global_vars['bastdata']['rego']
    data = global_vars['procdata']
    return itr.product(range(length), [data], [rego])


def fdins(N: note.Note, insre: re.Pattern) -> bool:
    '''
    Find Ins 
    Nums type list
    inse type str
    '''
    if insre == re.compile('(.*)'):
        # 不做任何限制
        return True
    else:
        try:
            Finx = len(insre.findall(N))
            return True if Finx >= 1 else False
        except re.error as rerror:
            return False


def combinations_ols(n, t, dr):
    zipo = ccp(n, t)
    for zio in zipo:
        if filter_map(zio, dr) == True:
            return True

    return False


def filter_map(zio, dr):
    data, rego = dr
    _n, _t = zio
    n = note.Note(_n, _t)
    rfilter = True
    if fdins(n, data['iRx']) == False:
        #print(f'debug fdins FALSE')
        return False
    if rego:
        for _, f in data['rego'].items():
            if f(n) == False:
                rfilter = False
                break
    for k, func in data['filter'].items():
        if func(n) == False:
            rfilter = False
            break
    return rfilter


def create(pcall_data: dict, rego: bool):  # -> list[Any] | None:
    if not pcall_data:
        print(f'Not Find PostCall Data!')
        return [0, [0], [0]]
    count = 0
    while 1:
        _n = pcall_data['glns']['r']()
        _t = pcall_data['glns']['b']()
        rfilter = combinations_ols(_n, _t, (pcall_data, rego))
        if rfilter == True:
            return [count, _n, _t]
        count += 1
        if count >= pcall_data['depth']:
            break
    return [count, [0], [0]]


def create_task(iq):
    task, pcall_data, rego = iq
    count, n, t = create(pcall_data, rego)
    return [task, count, n, t]


def tasks_single():
    global_vars = globals()
    length = global_vars['bastdata']['length']
    iStorage = []
    completed = 0
    sq3 = sq3database.Sqlite3Database()
    sq3.connect()
    if sq3.is_connected() == False:
        sq3.create_table_data()
    if sq3.is_Data_already_exists():
        sq3.clear_table_data()
    for i in initTaskQueue():
        rx = create_task(i)
        _, _, n, t = rx
        completed += 1
        if n != t:
            
            ns = ' '.join((f'{x:02}' for x in n))
            ts = ' '.join((f'{x:02}' for x in t))
            if sq3.check_data_r_number_exists(ns) == False:
                sq3.add_data(ns, ts)
        print(f'\033[K[P] completed {completed/length*100:.4f}% tasks completed.', end='\r')
    iStorage = sq3.read_data()
    sq3.disconnect()
    print(f'\033[K[P] completed. 100%')
    return iStorage if iStorage != None else []


def tasks_futures_old():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        iStorage = []
        results = executor.map(create_task, initTaskQueue())
        for res in results:
            _, _, n, t = res
            if n != t:
                iStorage.append(res)
    return iStorage

def tasks_futures():
    iStorage = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_task, i) for i in initTaskQueue()]
        completed = 0
        futures_len= futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            iStorage.append( future.result())
            print(f'\033[K[P] completed {completed/futures_len*100:.4f}% tasks completed.', end='\r')
        print(f'\033[K[P] completed. 100%')
    return iStorage if iStorage != None else []

def tasks_futures_press():
    iStorage = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_task, i) for i in initTaskQueue()]
        completed = 0
        sq3 = sq3database.Sqlite3Database()
        sq3.connect()
        sq3.create_table_data()
        sq3.clear_table_data()
        futures_len= futures.__len__()
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            _, _, n, t = future.result()
            if n != t:
                ns = ' '.join((f'{x:02}' for x in n))
                ts = ' '.join((f'{x:02}' for x in t))
                if sq3.check_data_r_number_exists(ns) == False:
                    sq3.add_data(ns, ts)
            print(f'\033[K[P] completed {completed/futures_len*100:.4f}% tasks completed.', end='\r')
        iStorage = sq3.read_data()
        print(f'\033[K[P] completed. 100%')
        sq3.disconnect()
    return iStorage if iStorage != None else []
