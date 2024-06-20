# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-12 20:39:38
from functools import partial
import os, collections, time
import re, itertools as itr, concurrent.futures
from typing import Callable, List, Iterable
from codex import BigLottery52_old, rego_v3, note, filters_v3, sq3database
from multiprocessing import Manager, Queue, cpu_count


bastdata = {"depth": 3000, "prompt": "[=]", "rego": False, "length": 25, "filter": True,}
procdata = {}


class pressecho:
    __map = collections.defaultdict(int)
    __max = 1000

    def __init__(self, length: int = 1000) -> None:
        self.__max = length

    def __str__(self) -> str:
        # print(f'{self.__map= }')
        # print('================================')
        values = sum(self.__map.values())
        bis = values / self.__max
        return f"mission completed {bis*100:.2f}%"

    def length(self, length: int = 1000):
        self.__max = length

    def clear(self):
        self.__map = collections.defaultdict(int)

    def put(self, pid):
        self.__map[pid] += 1


def ccp(a: Iterable, b: Iterable) -> itr.product:
    """ """
    Lir = itr.combinations(a, 6)
    Lib = itr.combinations(b, 1)
    zipo = itr.product(Lir, Lib)
    return zipo


def useRego(use: bool):
    """False rego NO"""
    global_vars = globals()
    global_vars["bastdata"]["rego"] = use
    return use


def useFilter(use: bool):
    """False rego NO"""
    global_vars = globals()
    global_vars["bastdata"]["filter"] = use
    return use


def settingLength(n: int = 25):
    """False rego NO"""
    global_vars = globals()
    global_vars["bastdata"]["length"] = n
    return n


def initPostCall(r: int, b: int, iRx: str):
    global_vars = globals()
    temp = {}
    fite = filters_v3
    fite.initialization()
    temp["rLen"] = r
    temp["bLen"] = b
    # temp["glns"] = glns_v2.glnsMpls(cdic, r, b, scw).producer
    temp["rego"], temp["product"] = rego_v3.Lexer().pares(rego_v3.load_rego_v2())
    temp["filter"] = fite.Checkfunc()
    temp["depth"] = global_vars["bastdata"]["depth"]
    temp["iRx"] = try_iRx(iRx=iRx)
    global_vars["procdata"] = temp


def try_iRx(iRx: str):
    try:
        _r = re.compile(iRx)
    except:
        _r = re.compile("(.*)")
    finally:
        return _r


def initTaskQueue_to_list():
    global_vars = globals()
    length = global_vars["bastdata"]["length"]
    rego = global_vars["bastdata"]["rego"]
    filterx = global_vars["bastdata"]["filter"]
    data = global_vars["procdata"]
    return length, data, rego, filterx


def fdins(N: note.Note, insre: re.Pattern) -> bool:
    """
    Find Ins
    Nums type list
    inse type str
    """
    if insre == re.compile("(.*)"):
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
    data, rego, filter = dr
    _n, _t = zio
    n = note.Note(_n, _t)
    rfilter = True
    if fdins(n, data["iRx"]) == False:
        # print(f'debug fdins FALSE')
        return False
    if rego:
        for _, f in data["rego"].items():
            if f(n) == False:
                rfilter = False
                break
    if filter:
        filterx = {name: func(n) for name, func in data["filter"].items()}
        # if filterx.count(False) > 1:
        #     rfilter = False
        match filterx:
            case {
                "acvalue": bool() as ac,
                "jmsht": bool() as five,
            } if ac == True and five == True:
                if sum(not value for value in filterx.values()) > 1:
                    # print(f'T, T {filterx}')
                    rfilter = False
            case {
                "acvalue": bool() as ac,
                "jmsht": bool() as five,
            } if ac == False or five == False:
                # print(f'F, _ {filterx}')
                rfilter = False
            case _:
                if sum(not value for value in filterx.values()) > 1:
                    # print(f'T, T {filterx}')
                    rfilter = False
    # for k, func in data['filter'].items():
    # if func(n) == False:
    #     rfilter = False
    #     break
    return rfilter


def mark_by_BigLotter52(conf):
    numx = BigLottery52_old.mark(config=conf)
    return numx["red"], numx["blue"]


def create(pcall_data: dict, rego: bool, filter: bool):  # -> list[Any] | None:
    if not pcall_data:
        print(f"Not Find PostCall Data!")
        return [0, [0], [0]]
    count = 0
    lr, lb = pcall_data["rLen"], pcall_data["bLen"]
    conf = {
        "red": partial(BigLottery52_old.coda_sec, rngs=range(1, 34), k=lr),
        "blue": partial(BigLottery52_old.coda_sec, rngs=range(1, 17), k=lb),
    }
    while 1:
        # ? 这里需要修改为 BigLottule
        # print(f'user BigLottule', end='\r')?
        _n, _t = mark_by_BigLotter52(conf)
        # _n = pcall_data["glns"]["r"]()
        # _t = pcall_data["glns"]["b"]()
        rfilter = combinations_ols(_n, _t, (pcall_data, rego, filter))
        if rfilter == True:
            return [count, _n, _t]
        count += 1
        if count >= pcall_data["depth"]:
            break
    return [count, [0], [0]]


def create_task(iq):
    task, pcall_data, rego, filter = iq
    count, n, t = create(pcall_data, rego, filter)
    return [task, count, n, t]


def create_task_v2(task: range, data, rego, filterx):
    stime = time.perf_counter()
    pf = lambda x: [x, *create(data, rego, filterx)]
    return [pf(x) for x in task], (time.perf_counter() - stime) / task.__len__()


def tasks_single():
    length, data, rego, filterx = initTaskQueue_to_list()
    iStorage = [None] * length
    seen_n = set()
    lr, lb = data["rLen"], data["bLen"]

    for index in range(length):
        rx = create(data, rego, filterx)
        # ? rx = {'red': [1, 3, 4, 15, 16, 33], 'blue': [5]}
        _, n, t = rx

        if n != t:
            ns = " ".join((f"{x:02}" for x in n))
            ts = " ".join((f"{x:02}" for x in t))
            if ns not in seen_n:
                iStorage[index] = [index, ns, ts]
                seen_n.add(ns)
                percentage = index / length
                # pass_e = "■" * (50 - pass_d.__len__())
                print(f"\033[0m+ generated {percentage * 100 :.2f}%", end="\r")
    # iStorage = sq3.read_data()
    # sq3.disconnect()
    print(f"There are `{length - iStorage.count(None)}` valid data generated")
    return [x for x in iStorage if x != None]


def done_task(future, storage: BigLottery52_old.jindu, seen: set):
    temp, ptime = future
    # print(f'{BigLottery52.sG(ptime)}', end='\r')
    for i in temp:
        # i = [58, 3000, [0], [0]]
        ids, deep, n, t = i
        if n != t:
            ns = " ".join((f"{x:02}" for x in n))
            ts = " ".join((f"{x:02}" for x in t))
            if ns not in seen:
                storage.Finished(ids, [ids, ns, ts])
                seen.add(ns)
        # pross(storage)


def tasks_from_regos():
    """通过rego 进行笛卡尔匹配"""
    global_vars = globals()
    product = global_vars["procdata"]["product"]
    iStorage = []
    _, data, rego, filterx = initTaskQueue_to_list()
    idx = 0
    for p_item in product.product():
        a, b, c, d, e, f, z = p_item
        if a < b < c < d < e < f:
            n = [a, b, c, d, e, f]
            t = [z]
            rfilter = combinations_ols([a, b, c, d, e, f], [z], (data, rego, filterx))

            if rfilter == True:
                iStorage.append([idx, n, t])
            idx += 1
        # print(f"{iStorage.__len__()}")
    return iStorage



def tasks_futures():
    '''新版本的 tasks_futures '''
    print(f'{BigLottery52_old.sY("tasks_futures is runing...")}')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        length, data, rego, filterx = initTaskQueue_to_list()
        jindux = BigLottery52_old.jindu(length)
        seen_n = set()
        chunk_size = length // cpu_count()
        _info = f"seting args {length} {chunk_size}"
        print(f"{BigLottery52_old.sY(_info)}")
        chunks = [
            range(length)[i : i + chunk_size] for i in range(0, length, chunk_size)
        ]
        futures = []
        for irng in chunks:
            futures.append(executor.submit(create_task_v2, irng, data, rego, filterx))
            
        for future in concurrent.futures.as_completed(futures):
            items = future.result()
            done_task(future=items, storage=jindux, seen=seen_n)
        jindux.echo(sda=0)
        
    print(f"There are `{length - jindux.block.count(None)}` valid data generated")
    return [x for x in jindux.block if isinstance(x, list)]


def tasks_futures_press():
    iStorage = tasks_futures()
    # with Manager() as me:
    sq3 = sq3database.Sqlite3Database()
    sq3.connect()
    sq3.create_table_data()
    sq3.clear_table_data()
    for i in iStorage:
        ids, n, t = i
        sq3.add_data(n, t)
    sq3.disconnect()
    return iStorage if iStorage != None else []
