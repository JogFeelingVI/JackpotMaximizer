# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-18 08:58:03
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-15 16:44:20
import multiprocessing, os, time, re, logging, random, concurrent.futures, pathlib, itertools, secrets, inspect
from dataclasses import dataclass
from functools import partial
from typing import Callable, List, Any

__version__ = '0.1.2'

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
        self.block = []
        self.echotime = time.perf_counter()
        self.lock = multiprocessing.Lock()
        self.press = ""

    def Finished(self, value):
        with self.lock:
            try:
                self.block.append(value)
            except:
                pass
            finally:
                self.echo()

    def echo(self, sda=9):
        if (nt := time.perf_counter() - self.echotime) > 0.3 or sda == 0:
            pe = self.block.__len__() / self.length
            pe_d = "■" * int(50 * pe)
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

def filters(config:dict = {}, item:dict={}):
    '''
    启动过滤器
    '''
    # item={'red': [2, 11, 17, 23, 26, 33], 'bule': [7]}
    Target = config.get('Target')
    # print(f'debug -> {config}')
    # return
    if Target:
        funi = [p for k,p in config.items() if k != 'Target']
        bn = item[Target]
        bn_coda = codafmt(bn).filter(func=funi)
        if bn_coda:
            # print(f'filter keys {item.keys()}')
            return item
        else:
            return None
    return None


def Processor_rng(func: Callable, irangs, config: dict = {}, ):
    """
    {
        'bule':coda(rngs,k=5), yellow: coda(rngs,k=2)
    }
    """
    signature = inspect.signature(func)
    parameters = signature.parameters
    
    match list(parameters.keys()):
        case ['config']:
            p = lambda x: func(config=config)
        case ['config', 'item']:
            p = lambda i: func(config=config, item=i)
    return [p(i) for i in irangs]


def done(items, numbers: jindu):
    for item in items:
        if item:
            numbers.Finished(value=item)


def display(**kwargs):
    '''
    显示 最终结果
    bn = item["bule"]
    bn_coda = BigLottery52.codafmt(bn)
    '''
    fmt = kwargs.get('FMT')
    pz = kwargs.get('PZ')
    result = kwargs.get('result')
    if fmt and pz and result:
        for item in result:
            itemEx = {}
            for p,z in pz.items():
                if p in item.keys():
                    itemEx.update({p:codafmt(item[p], z)})
                else:
                    raise Exception(f'{p} Wrong parameter configuration. IN [{' '.join(item.keys())}].')
            print(fmt.format(**itemEx))
            
    else:   
        print(f'{fmt =} {pz =}')

def DataProcessor(**kwargs):
    '''
    kwargs is Dict
        exp {'config':'CONF','funx':BigLottery52.mark, 'length':5*1*10000}
    '''
    config = kwargs.get('config')
    funx = kwargs.get('funx')
    result = kwargs.get('result')
    length = kwargs.get('length')
    #? 这里 jindux = jindu(length)
    if length and result == None:
        jindux = jindu(length)
        chunk_size = length // cpus
        if chunk_size != 0:
            chunks = [
            range(length)[i : i + chunk_size] for i in range(0, length, chunk_size)
        ]
        else:
            chunks = [[i] for i in range(0, length)]
    elif length == None and result:
        length = len(result)
        jindux = jindu(length)
        chunk_size = length // cpus
        if chunk_size != 0:
            chunks = [
            result[i : i + chunk_size] for i in range(0, length, chunk_size)
        ]
        else:
            chunks = [[x] for x in result]
    #? 目前位置 到这里是正常的
    futures = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        if config and funx:
            for rng in chunks:
                #! 检测这里是否正确
                futures.append(executor.submit(Processor_rng, funx, rng, config))
            init_info = f"Initialization futures, index {futures.__len__()}"
            print(f"{sG(init_info)}")
            for future in concurrent.futures.as_completed(futures):
                items = future.result()
                
                done(items=items, numbers=jindux)
        jindux.echo(sda=0)
    tips = f"data factory all done {jindux.block.__len__():,}"
    print(f"{sB(tips)}")
    return jindux.block


def execute_process(process:List[dict[str, Any]]):
    '''
    execute_process
        [
            {
                type: initialization
                work: function
                args: {k=10}
                callback: function
            }
        ]
    
    function_type
        initialization 初始化程序执行的基本数据
        create 创建数据
        filter 过滤内容
        display 展示成果
    
    dict
        type function_type
    '''
    data = {'TIME':time.perf_counter()}
    result = []
    for step in process:
        step_type = step.get("type")
        step_work = step.get('work')
        step_args = step.get("args" )
        callback = step.get("callback")
        
        match step_type:
            case 'initialization':
                if step_work:
                    if step_args:
                        data.update(step_work(step_args))
                    else:
                        data.update(step_work())
                init_info = f'Initialization of workflow basic variables has been completed.\n  -> {' '.join(data.keys())}'
                print(f'{sB(init_info)}')
            case 'create'| 'filter':
                if step_work and step_args:
                    try:
                        #! 判断 step_args 类型
                        match step_args:
                            case dict() as kw:
                                for k, v in kw.items():
                                    if isinstance(v, str):
                                        kw.update({k:data.get(v, v)})
                                if step_type == 'filter':
                                    if result:
                                        kw.update({'result': result})
                                    else:
                                        break
                                result = step_work(**kw)
                            case _ as args:
                                result = step_work(args)
                            
                        if callback and result:
                            callback(result)
                    except Exception as e:
                        err_info = f'{step_type} Workflow Errors, fun_work(args).\n  -> {e}'
                        print(f'{sR(err_info)}')
                    else:
                        done_info= f'Workflow `{step_type}` has completed. No exceptions were found.'
                        print(f'{sY(done_info)}')
            case 'display':
                #? 这里开始执行显示程序    
                if step_work and step_args:
                    #! 判断 step_args 类型
                    try:
                        match step_args:
                            case dict() as kw:
                                for k, v in kw.items():
                                    if isinstance(v, str):
                                        kw.update({k:data.get(v, v)})
                                if result:
                                    kw.update({'result': result})
                                    step_work(**kw)
                                if callback and result:
                                    callback(result)
                            case _ as args:
                                raise Exception(f'Wrong parameter type, <args_type:{type(step_args).__name__}>.')
                    except Exception as e:
                        err_info = f'{step_type} Workflow Errors, fun_work(args).\n  -> {e}'
                        print(f'{sR(err_info)}')
                    else:
                        done_info= f'Workflow `{step_type}` has completed. No exceptions were found.'
                        print(f'{sY(done_info)}')
            case 'other':
                if step_work and step_args:
                    #! 判断 step_args 类型
                    try:
                        match step_args:
                            case dict() as kw:        
                                kw.update({'result': result})
                                temp = step_work(**kw)
                                if callback and temp:
                                    callback(temp)
                            case _ as args:
                                raise Exception(f'Wrong parameter type, <args_type:{type(step_args).__name__}>.')
                    except Exception as e:
                        err_info = f'{step_type} Workflow Errors, fun_work(args).\n  -> {e}'
                        print(f'{sR(err_info)}')
                    else:
                        done_info= f'Workflow `{step_type}` has completed. No exceptions were found.'
                        print(f'{sY(done_info)}')
            case _:
                print(f'execute_process configuration error. {step_type}')
