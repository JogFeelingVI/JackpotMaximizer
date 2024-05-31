# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-18 08:58:03
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-31 23:24:12
import collections, os, time, re, logging, random, concurrent.futures, pathlib, itertools, secrets
from dataclasses import dataclass
from functools import partial
from typing import Callable, List

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
debug = "vv"
cpus = cpn if (cpn:=os.cpu_count()) != None else 4

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
sR = lambda s: f"{RED}{s}{ENDC}"
sY = lambda s: f"{YELLOW}{s}{ENDC}"
sB = lambda s: f"{BLUE}{s}{ENDC}"
sG = lambda s: f"{GREEN}{s}{ENDC}"


@dataclass
class codafmt:

    def filter(self, func):
        """
        func is Callable
        """
        if isinstance(func, Callable):
            func = [func]

        if isinstance(func, list):
            if not all(isinstance(item, Callable) for item in func):
                raise TypeError("All elements in parameter `func` must be Callable.")

        for filter_func in func:
            if not filter_func(n=self.Zone):
                return False

        return True

    def __str__(self) -> str:
        bzs = self.__tos(self.Zone)
        return f"{self.shader(bzs)}"

    @staticmethod
    def __tos(Lis: list[int], split: str = " ") -> str:
        temp = [f"{x:02}" for x in Lis]
        return split.join(temp)

    def __init__(self, data: List[int], shader: Callable = sB):
        """
        data List int
        func = r|b|y|g
        """
        if not isinstance(data, list):
            raise TypeError("Parameter 'data' must be a list.")

        if not all(isinstance(item, int) for item in data):
            raise TypeError("All elements in parameter 'data' must be integers.")

        if shader is not None and not callable(shader):
            raise TypeError("Argument `func` must be a callable function.")
        self.Zone = data
        self.shader = shader


def coda(rngs: list | range, k: int = 2):
    match rngs:
        case range() as rng:
            numbers = [x for x in rng]
        case list() as lis:
            numbers = []
            for iL in lis:
                match iL:
                    case int() as n:
                        numbers.append(n)
                    case list() | tuple() as n:
                        numbers.extend(n)
                    case range() as r:
                        numbers.extend((x for x in r))
    # print(f'{numbers = }')
    random.shuffle(numbers)
    return sorted(numbers[:k])

def coda_sec(rngs: list | range, k: int = 2):
    match rngs:
        case range() as rng:
            numbers = [x for x in rng]
        case list() as lis:
            numbers = []
            for iL in lis:
                match iL:
                    case int() as n:
                        numbers.append(n)
                    case list() | tuple() as n:
                        numbers.extend(n)
                    case range() as r:
                        numbers.extend((x for x in r))
    random.shuffle(numbers)
    codae = set()
    while len(codae) < k:
        index = secrets.randbelow(len(numbers))
        codae.add(numbers[index])
        del numbers[index]
        random.shuffle(numbers)
    return sorted(list(codae))
        
def mark(config:dict = {}):
    keys = config.keys()
    temp = dict().fromkeys(keys, [])
    for k, funx in config.items():
        temp[k] = funx()
    if debug.count("v") == 3:
        print(f"mark_by config {config}\n{temp}")
    return temp


def mark_by(config: dict = {}, irangs:range=range(1, 1000)):
    """
    {
        'bule':coda(rngs,k=5), yellow: coda(rngs,k=2)
    }
    """
    iRngs = []    
    for i in irangs:
        iRngs.append((i, mark(config=config)))
    return iRngs


def done(future, numbers: list, length: int):
    items = future.result()
    for idx, item in items:
        numbers.append(item)
        pass_d = "■" * int(50 * numbers.__len__() / length)
        pass_e = "■" * (50 - pass_d.__len__())
        print(f"{ENDC}+ {sB(pass_d)}{pass_e}", end="\r")


def data_factory(config: dict, length: int = 500):
    print(sY('Prepare multi-threaded environment, please wait...'), end='\r')
    numbers = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        chunk_size = length // cpus
        chunks = [
                range(length)[i : i + chunk_size] for i in range(0, length, chunk_size)
            ]
        futures = [
            executor.submit(mark_by, config, i).add_done_callback(
                lambda future: done(future, numbers, length)
            )
            for i in chunks
        ]
    # numbers = mark_by(congfig=config)
    tips = f"data factory all done {length}"
    print(' ' * 52,end='\r')
    print(f'{sY(tips)}')
    return numbers




