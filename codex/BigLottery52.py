# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-18 08:58:03
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-07 09:30:47
import multiprocessing, os, time, re, logging, random, concurrent.futures, pathlib, itertools, secrets
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
cpus = cpn if (cpn := os.cpu_count()) != None else 4

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


class jindu:
    def __init__(self, length: int = 1000) -> None:
        self.length = length
        self.block = [None] * length
        self.echotime = time.perf_counter()
        self.lock = multiprocessing.Lock()
        self.press = ""

    def Finished(self, index: int, value):
        with self.lock:
            try:
                self.block[index] = value
            except:
                pass
            finally:
                self.echo()

    def echo(self, sda=9):
        if (nt := time.perf_counter() - self.echotime) > 0.3 or sda == 0:
            pe = (self.length - self.block.count(None)) / self.length
            pe_d = "■" * int(pe * 50)
            self.echotime = time.perf_counter()
            self.press = f"{ENDC}DataFactory {pe_d} {pe * 100 :.2f}%"
            if sda > 0:
                print(f"{self.press}", end="\r")
            else:
                print(f"{self.press} END")


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
    # random.shuffle(numbers)
    codae = set()
    while len(codae) < k:
        index = secrets.randbelow(len(numbers))
        codae.add(numbers[index])
        del numbers[index]
        # random.shuffle(numbers)
    return sorted(list(codae))


def mark(config: dict = {}):
    """具体执行过程 在封装"""
    keys = config.keys()
    temp = dict().fromkeys(keys, [])
    for k, funx in config.items():
        temp[k] = funx()
    if debug.count("v") == 3:
        print(f"mark_by config {config}\n{temp}")
    return temp


def mark_by(func: Callable, config: dict = {}, irangs: range = range(1, 1000)):
    """
    {
        'bule':coda(rngs,k=5), yellow: coda(rngs,k=2)
    }
    """
    p = lambda x: (x, func(config=config))
    return [p(i) for i in irangs]


def done(items, numbers: jindu):
    for idx, item in items:
        numbers.Finished(index=idx, value=item)


def data_factory(
    config: dict,
    makrfun: Callable = mark,
    length: int = 500,
):
    print(sY("Prepare multi-threaded environment, please wait..."))
    # numbers = [None] * length
    jindux = jindu(length)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        chunk_size = length // cpus
        chunks = [
            range(length)[i : i + chunk_size] for i in range(0, length, chunk_size)
        ]
        futures = []
        for rng in chunks:
            futures.append(executor.submit(mark_by, makrfun, config, rng))
        init_info = f"Initialization futures, index {futures.__len__()}"
        print(f"{sG(init_info)}")
        for future in concurrent.futures.as_completed(futures):
            items = future.result()
            done(items=items, numbers=jindux)
        jindux.echo(sda=0)

    tips = f"data factory all done {length:,}"
    print(f"{sB(tips)}")
    return jindux.block
