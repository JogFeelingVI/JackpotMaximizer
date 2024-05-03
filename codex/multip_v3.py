# @Author: JogFeelingVi
# @Date: 2023-03-23 22:38:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-04 00:43:24
import os, collections
import re, itertools as itr, concurrent.futures
from typing import Callable, List, Iterable
from codex import glns_v2, rego_v3, note, filters_v3, sq3database
from multiprocessing import Manager, Queue, cpu_count


bastdata = {"depth": 3000, "prompt": "[=]", "rego": False, "length": 25, "filter": True}
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


def initPostCall(cdic: dict, r: int, b: int, iRx: str, scw: str):
    global_vars = globals()
    temp = {}
    fite = filters_v3
    fite.initialization()
    temp["glns"] = glns_v2.glnsMpls(cdic, r, b, scw).producer
    temp["rego"] = rego_v3.Lexer().pares(rego_v3.load_rego_v2())
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


def initTaskQueue():
    global_vars = globals()
    length = global_vars["bastdata"]["length"]
    rego = global_vars["bastdata"]["rego"]
    filter = global_vars["bastdata"]["filter"]
    data = global_vars["procdata"]
    return itr.product(range(length), [data], [rego], [filter])


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


def create(pcall_data: dict, rego: bool, filter: bool):  # -> list[Any] | None:
    if not pcall_data:
        print(f"Not Find PostCall Data!")
        return [0, [0], [0]]
    count = 0
    while 1:
        _n = pcall_data["glns"]["r"]()
        _t = pcall_data["glns"]["b"]()
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


def create_task_v2(task: range, data, rego, filterx, pd:dict):
    temp = []
    pid = os.getpid()
    for task_index in task:
        if pid in pd.keys():
            pd[pid] += 1
        else:
            pd[pid] = 1
        sumx = sum(pd.values())
        temp.append([task_index, *create(data, rego, filterx)])
        if task_index % 5 == 1:
            print(f"\033[K[P] mission completed {sumx}", end="\r")
    return temp, pid


def tasks_single():
    global_vars = globals()
    length = global_vars["bastdata"]["length"]
    iStorage = []
    seen_n = set()
    # sq3 = sq3database.Sqlite3Database()
    # sq3.connect()
    # if sq3.is_connected() == False:
    #     sq3.create_table_data()
    # if sq3.is_Data_already_exists():
    #     sq3.clear_table_data()
    length, data, rego, filterx = initTaskQueue_to_list()
    for index in range(length):
        rx = create(data, rego, filterx)
        _, n, t = rx
        if n != t:
            ns = " ".join((f"{x:02}" for x in n))
            ts = " ".join((f"{x:02}" for x in t))
            if ns not in seen_n:
                iStorage.append([index, ns, ts])
                seen_n.add(ns)
        print(f"\033[K[P] completed {index/length*100:.4f}% tasks completed.", end="\r")
    # iStorage = sq3.read_data()
    # sq3.disconnect()
    print(f"\033[K[P] completed. 100%")
    return iStorage if iStorage != None else []


def done_task(future, storage: List, seen: set):
    temp, pid = future.result()
    
    count = 0
    for i in temp:
        # i = [58, 3000, [0], [0]]
        ids, deep, n, t = i
        if n != t:
            ns = " ".join((f"{x:02}" for x in n))
            ts = " ".join((f"{x:02}" for x in t))
            if ns not in seen:
                storage.append([ids, ns, ts])
                seen.add(ns)
                count += 1
        # print(f"\033[K[P] {echo}", end="\r")
    # print(f"Complete effective tasks {count} from worker-{pid}")


def tasks_futures():
    iStorage = []
    seen_n = set()
    with Manager() as mem:
        pd = mem.dict(collections.defaultdict(int))
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            length, data, rego, filterx = initTaskQueue_to_list()
            chunk_size = length // cpu_count()
            chunks = [
                range(length)[i : i + chunk_size] for i in range(0, length, chunk_size)
            ]
            futures = [
                executor.submit(create_task_v2, i, data, rego, filterx, pd).add_done_callback(
                    lambda f: done_task(f, iStorage, seen_n)
                )
                for i in chunks
            ]

    return iStorage if iStorage != None else []


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
