# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-09-12 08:47:23
# @Last Modified by:   Your name
# @Last Modified time: 2024-11-13 16:06:54

from itertools import zip_longest
from typing import List
import tqdm, time, random, datetime
from codex import multip_v4

NxCU = [1, 2, 4, 3, 6, 7, 8, 9, 0, 11, 23]
ARGS = {"n": 1000, "loadins": True, "loadfilter": True}
idex_range = [x for x in range(0, 10000)]


def Lastime(timex) -> str:
    """
    @Last Modified time: 2023-11-21 10:32:45
    """
    match timex:
        case None:
            now = datetime.datetime.now()
        case datetime.datetime() as dd:
            now = dd
        case _:
            now = datetime.datetime.now()
    # 格式化时间字符串
    formatted_time = now.strftime("@Last Modified time: %Y-%m-%d %H:%M:%S")
    return formatted_time


def connToStr(item: list | dict):
    """connToStr {'red': [3, 13, 15, 24, 27, 32], 'bule': [11], 'id': '25', 'logs': 18}"""
    match item:
        case list() as Li:
            fromid, n, t, dfr4, dfr5, timex = Li
            dic = {"dfr": [dfr4, dfr5]}
            return f"{Lastime(timex)} -> id {fromid:>4} / cyn {dic} * {n} + {t}"

        case dict() as Di:
            # multip_v4.BigLottery52.logger.info(f'{Di.keys()}')
            keys = ["red", "bule", "id", "logs", "time", "dfr"]
            values = [Di[k] for k in keys]
            n, t, id, logs, timex, dfr = values
            dic = {"dif": logs,"dfr":dfr}
            return f"{Lastime(timex)} -> id {id:>4} / logs {dic} * {n} + {t}"

        case _:
            return f"{Lastime()} -> Error {item}"


def convtodict(item: list, id: int):
    """
    data.append({"red": ast.literal_eval(_r), "bule": ast.literal_eval(_b), "id":_id, "logs":0})
    {'red': [2, 15, 17, 24, 27, 32], 'bule': [11], 'id': '01', 'logs': 0}
    """
    _, n, t, dfr4, dfr5, timing = item
    # multip_v4.BigLottery52.logger.info(f'{n} + {t} {timing}')
    return {"red": n, "bule": t, "id": id, "logs": 0, "time": timing}

def addList(a:List[int], b:List[int]) -> List[int]:
    return [x + y for x, y in zip_longest(a, b, fillvalue=0)]

def remove_duplicates(data, key):
    """
    过滤列表中的重复字典项，保留第一个出现的字典。

    Args:
        data: 要过滤的字典列表。
        key: 用于判断重复的键。

    Returns:
        过滤后的字典列表。
    """
    seen = set()
    result = []
    for item in data:
        # 使用键值作为判断依据
        key_value = [f'{x}' for x in item[key] ]
        key_value = ''.join(key_value)
        if key_value not in seen:
            seen.add(key_value)
            result.append(item)
    return result


def main(explore: int = 25, load: int = 25, exp: str = "./exp", lod: str = "./lod"):
    startme = datetime.datetime.now()
    exp_ram = []
    p = multip_v4
    p.initialization(conf=ARGS)
    with tqdm.tqdm(total=explore, desc="Explore", colour="red", ascii=True) as pbar:
        while True:
            Retds = p.tasked_nop()
            pbar.total = exp_ram.__len__() + Retds.__len__()
            pbar.update(Retds.__len__())
            if Retds:
                exp_ram.extend(Retds)
            if exp_ram.__len__() >= explore:
                break

    exp_data = []
    # 队列已满，可以进行后续操作 写入文件
    with open(exp, "w") as file:
        for item in tqdm.tqdm(exp_ram, desc="Save To", colour="blue", ascii=True):
            idx = idex_range[0]
            idex_range.remove(idx)
            change_item = convtodict(item, idx)
            file.write(f"{connToStr(item)}\n")
            exp_data.append(change_item)
    exp_ram.clear()

    # 开始穿透
    def recyns(p: str):
        # 读取数据
        # print(f'{p = } -> {exp_data[0]}')
        return remove_duplicates(exp_data, 'red')

    count = 0
    with tqdm.tqdm(total=load, desc="loAD Progress", colour="CYAN", ascii=True) as pbar:
        while True:
            Retds = p.loadtask(loadlog=recyns)
            if Retds:
                idx = {k["id"]:k for k in Retds}
                dfrkeys = set([k for x in Retds for k in dict(x).keys() if 'DFR' in k])
                for cd in exp_data:
                    if (id:=cd['id']) in idx.keys():
                        cd["logs"] += 1
                        RetdsId = idx[id]
                        if RetdsId != None:
                            dfrs = [RetdsId[k] for k in dfrkeys]
                            cd.update({'dfr':addList(cd.get('dfr',[]),dfrs)})

            pbar.update()
            count += 1
            if count >= load:
                break
    # 写入logs 文件
    exp_data = [x for x in exp_data if x['logs']>=1]
    exp_data = sorted(exp_data, key=lambda item: (-item["logs"], item["dfr"][0]))
    with open(lod, "w") as file:
        for item in tqdm.tqdm(exp_data, desc="logs To", colour="MAGENTA", ascii=True):
            file.write(f"{connToStr(item)}\n")
    print(
        f"EXL parameters are {explore} LOD parameters are {load}, the total program time is {datetime.datetime.now() - startme} seconds"
    )


if __name__ == "__main__":
    explore = 100
    load = 10
    save_exp = "./cyns.log"
    save_lod = "./load.log"
    main(explore, load, save_exp, save_lod)
