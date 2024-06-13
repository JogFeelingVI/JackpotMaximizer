# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-11 22:08:55
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-13 16:18:38

from functools import partial
import re
from codex import BigLottery52, filters_v4, rego_v3

config = {
    "depth": 3000,
    "n": 25,
    "loadins": True,
    "filter": True,
    "ins": "(.*)",
    "r": 6,
    "b": 1,
    "execute_process": None,
}


def __init_Config(conf: dict):
    global config
    if conf:
        config.update(conf)


def __init_PostCall():
    global config
    temp = {}
    
    temp["rego"], temp["product"] = rego_v3.Lexer().pares(rego_v3.load_rego_v2())
    temp["ins"] = __ConversionRegx(config.get("ins", "(.*)"))
    config.update(temp)


def __init_conf():
    global config
    r = config.get("r", 6)
    b = config.get("b", 1)
    config = {
        "red": partial(BigLottery52.coda_sec, rngs=range(1, 34), k=r),
        "bule": partial(BigLottery52.coda_sec, rngs=range(1, 17), k=b),
    }
    strfmt = "SSQ coda {red} + {bule}"
    return {"CONF": config, "FMT": strfmt}

def __init_filter():
    global config
    filter = filters_v4
    filter.initialization()
    temp = filter.Checkfunc()
    temp.update({"Target": "red"})
    return {'FILTER':temp}


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


def tasked():
    global config
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
        {"type": "initialization", "work": __init_filter},
        {
            "type": "filter",
            "work": BigLottery52.DataProcessor,
            "args": {"config": "FILTER", "funx": BigLottery52.filters},
            "callback": lambda re: print(f"FILTER Callback: {re[0]}"),
        },
        {
            "type": "display",
            "work": BigLottery52.display,
            "args": {
                "FMT": "FMT",
                "PZ": {"red": BigLottery52.sR, "bule": BigLottery52.sG},
            },
        },
    ]
    BigLottery52.execute_process(process=temp)


def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
