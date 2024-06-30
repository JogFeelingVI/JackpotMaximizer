# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-11 22:08:55
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-30 13:59:25

from functools import partial
import re, itertools
from typing import Iterable
from codex import BigLottery52, filters_v4, rego_v4

config = {
    "depth": 3000,
    "n": 25,
    "loadins": False,
    "loadfilter": True,
    "ins": "(.*)",
    "r": 6,
    "b": 1,
}


def __init_Config(conf: dict):
    global config
    if conf:
        config.update(conf)


def __init_PostCall():
    global config
    temp = {}
    temp["ins"] = __ConversionRegx(config.get("ins", "(.*)"))
    if config.get("loadins"):
        rego, product = rego_v4.Lexer().pares(rego_v4.load_rego_v2())
        temp["rego"] = rego
        temp["product"] = product
    config.update(temp)


def __init_conf():
    global config
    r = config.get("r", 6)
    b = config.get("b", 1)
    itemJg = {
        "red": partial(BigLottery52.coda_sec, rngs=range(1, 34), k=r),
        "bule": partial(BigLottery52.coda_sec, rngs=range(1, 17), k=b),
    }
    strfmt = "SSQ coda {red} + {bule}"
    return {"CONF": itemJg, "FMT": strfmt}


def __init_filter():
    global config
    temp = {}
    if config.get("loadfilter"):
        filter = filters_v4
        filter.initialization()
        temp = filter.Checkfunc()
    temp.update({"Target": "red"})
    return {"FILTER": temp}


def __init_rego(tar: str):
    """rego to"""
    global config
    temp = config.get("rego")
    rego = {"Target": tar}
    match tar:
        case "red":
            indexs = [1, 2, 3, 4, 5, 6]
        case "bule":
            indexs = [7]
    if config.get('loadins'):
        if temp:
            for k, partial_func in temp.items():
                if partial_func.keywords["index"] in indexs:
                    rego[k] = partial_func
    return {"FILTER": rego}


def __ConversionRegx(ins):
    try:
        _r = re.compile(ins)
    except:
        _r = re.compile("(.*)")
    finally:
        return _r


def initialization(conf: dict):
    """
    跟新系统默认值 使用 conf
    # initialization_data = {
    #     "config": lambda conf: __initConfig(conf=conf),
    #     "PostCall": lambda x: __initPostCall(),
    #     "process": lambda x: __initProcess(),
    # }
    """
    initialization_data = [
        {"name": "config", "work": __init_Config, "args": conf},
        {"name": "PostCall", "work": __init_PostCall},
    ]
    for item in initialization_data:
        try:
            name = item.get("name")
            work = item.get("work")
            args = item.get("args")
            if work:
                if args:
                    work(args)
                else:
                    work()
            print(f"initialization {name} Done.")
        except Exception as e:
            print(f"initialization {name} Error.\n  -> {e}")


def formmattolist(**kwargs):
    """
    格式转换 format 'index,red,bule'
    """
    format = kwargs.get("format")
    result = kwargs.get("result")
    result_to = []
    if format and result:
        geshi = str(format).split(",")
        for index, res_item in enumerate(result):
            n = []
            for _f in geshi:
                match _f:
                    case "index":
                        n.append(index)
                    case str() as keys:
                        n.append(res_item.get(keys))
            result_to.append(n)
    return result_to


def tasked():
    global config
    tasked_data = []
    temp: list = [
        {"type": "initialization", "work": __init_conf},
        {
            "type": "create",
            "work": BigLottery52.DataProcessor,
            "args": {
                "config": "CONF",
                "funx": BigLottery52.mark,
                "length": config.get("n", 25),
            },
            "callback": lambda re: print(f"Callback: {re[0]}"),
        },
        {"type": "initialization", "work": lambda: __init_rego("red")},
        {
            "type": "filter",
            "work": BigLottery52.DataProcessor,
            "args": {"config": "FILTER", "funx": BigLottery52.filters},
            "callback": lambda re: print(f"Rego Callback: {re[0]}"),
        },
        {"type": "initialization", "work": lambda: __init_rego("bule")},
        {
            "type": "filter",
            "work": BigLottery52.DataProcessor,
            "args": {"config": "FILTER", "funx": BigLottery52.filters},
            "callback": lambda re: print(f"REGO Callback: {re[0]}"),
        },
        {"type": "initialization", "work": __init_filter},
        {
            "type": "filter",
            "work": BigLottery52.DataProcessor,
            "args": {"config": "FILTER", "funx": BigLottery52.filters},
            "callback": lambda re: print(f"FILTER Callback: {re[0]}"),
        },
        #! 新的filter 初始化工作
        {
            "type": "differ",
            "work": BigLottery52.DataProcessor,
            "args": {
                "step1": {"config": "CONF", "funx": BigLottery52.mark, "length": 10000},
                "step2": {
                    "Probability": ["red", 4, 0.0047, 0.0001],
                    "funx": BigLottery52.differ,
                },
                "step3": {
                    "Probability": ["red", 5, 0.0001, 0.0001],
                    "funx": BigLottery52.differ,
                }
            },
            "callback": lambda re: print(f"FILTER differ Callback: {re[0]}"),
        },
        {
            "type": "other",
            "work": formmattolist,
            "args": {"format": "index,red,bule"},
            "callback": lambda re: tasked_data.extend(re),
        },
    ]
    BigLottery52.execute_process(process=temp)
    return tasked_data


def ccp(a: Iterable, b: Iterable) -> itertools.product:
    """ """
    Lir = itertools.combinations(a, 6)
    Lib = itertools.combinations(b, 1)
    zipo = itertools.product(Lir, Lib)
    return zipo


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
