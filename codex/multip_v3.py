# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-02-28 23:22:06
from datetime import datetime as dtime
import re, itertools as itr, concurrent.futures
from typing import List, Iterable
from codex import glns_v2, rego_v3, note, filters_v3

bastdata = {
    'depth': 3000,
    'prompt': '[=]',
    'rego': False,
    'length': 25
}
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


def initPostCall(cdic: dict, r: int, b: int, iRx: re.Pattern, scw: str):
    global_vars = globals()
    temp = {}
    fite = filters_v3
    fite.initialization()
    temp['glns'] = glns_v2.glnsMpls(cdic, r, b, scw).producer
    temp['rego'] = rego_v3.Lexer().pares(rego_v3.load_rego_v2())
    temp['filter'] = fite.Checkfunc()
    temp['depth'] = global_vars['bastdata']['depth']
    temp['iRx'] = iRx
    global_vars['procdata'] = temp


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
        return [0, [0],[0]]
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
    return [count, [0],[0]]


def create_task(iq):
    task, pcall_data, rego = iq
    count, n, t = create(pcall_data, rego)
    return [task, count, n, t]


def tasks_single():
    iStorage = []
    for i in initTaskQueue():
        rx = create_task(i)
        _, _, n, t= rx
        if n != t:
            iStorage.append(rx)
    return iStorage 

def tasks_futures():
    with concurrent.futures.ProcessPoolExecutor() as cfp:
        iStorage = []
        results = cfp.map(create_task, initTaskQueue())
        for res in results:
            _, _, n, t= res
            if n!=t:
                iStorage.append(res)
    return iStorage

