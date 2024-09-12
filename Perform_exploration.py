# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-09-12 08:47:23
# @Last Modified by:   Your name
# @Last Modified time: 2024-09-12 21:10:41

import tqdm, time, random, datetime
from codex import multip_v4

NxCU = [1, 2, 4, 3, 6, 7, 8, 9, 0, 11, 23]
ARGS = {"n": 1000, "loadins": True, "loadfilter": True}
idex_range = [f"{x:02}" for x in range(1, 10000)]

def Lastime() -> str:
    """
    @Last Modified time: 2023-11-21 10:32:45
    """
    now = datetime.datetime.now()
    # 格式化时间字符串
    formatted_time = now.strftime("@Last Modified time: %Y-%m-%d %H:%M:%S")
    return formatted_time


def connToStr(item:list|dict):
    '''connToStr {'red': [3, 13, 15, 24, 27, 32], 'bule': [11], 'id': '25', 'logs': 18}'''
    match item:
        case list() as Li:
            fromid, n, t, dfr4, dfr5 = Li
            dic = {4: dfr4, 5: dfr5}
            return f"{Lastime()} -> id {fromid:>4} / cyn {dic} * {n} + {t}"
        
        case dict() as Di:
            n, t, id, logs = Di.values()
            dic = {4: logs}
            return f"{Lastime()} -> id {id:>4} / logs {dic} * {n} + {t}"
        
        case _:
            return f"{Lastime()} -> Error {item}"


def convtodict(item: list, id: str):
    """
    data.append({"red": ast.literal_eval(_r), "bule": ast.literal_eval(_b), "id":_id, "logs":0})
    {'red': [2, 15, 17, 24, 27, 32], 'bule': [11], 'id': '01', 'logs': 0}
    """
    _, n, t, dfr4, dfr5 = item
    return {"red": n, "bule": t, "id": id, "logs": 0}


def main(explore: int = 25, load: int = 25, exp: str = "./exp", lod: str = "./lod"):
    startme = datetime.datetime.now()
    exp_ram = []
    p = multip_v4
    p.initialization(conf=ARGS)
    with tqdm.tqdm(total=explore, desc="Explore Progress", colour='red', ascii=True) as pbar:
        while True:
            Retds = p.tasked_nop()
            pbar.update()
            if Retds:
                exp_ram.extend(Retds)
            if exp_ram.__len__() >= explore:
                break

    exp_data = []
    # 队列已满，可以进行后续操作 写入文件
    with open(exp, "w") as file:
        for item in tqdm.tqdm(exp_ram, desc="Save To", colour='blue', ascii=True):
            file.write(f"{connToStr(item)}\n")
            idx = idex_range[0]
            idex_range.remove(idx)
            exp_data.append(convtodict(item, idx))
    # 开始穿透
    def recyns(p:str):
        # 读取数据
        # print(f'{p = } -> {exp_data[0]}')
        return exp_data
    
    count =0 
    with tqdm.tqdm(total=load, desc="loAD Progress", colour='CYAN', ascii=True) as pbar:
        while True:
            Retds = p.loadtask(loadlog=recyns)
            if Retds:
                # print(f'{Retds.__len__()} {Retds[0]}')
                for rix in Retds:

                    find_id = dict(rix).get("id", "")
                    for cd in exp_data:
                        if cd["id"] == find_id:
                            cd["logs"] += 1
            pbar.update()
            count+=1
            if count >= load:
                break
    # 写入logs 文件
    exp_data = sorted(exp_data, key=lambda item: item["logs"], reverse=True)
    with open(lod, "w") as file:
        for item in tqdm.tqdm(exp_data, desc="logs To", colour='MAGENTA', ascii=True):
            file.write(f"{connToStr(item)}\n")
    print(f'EXL parameters are {explore} LOD parameters are {load}, the total program time is {datetime.datetime.now() - startme} seconds')


if __name__ == "__main__":
    explore = 30
    load = 30
    save_exp = "./cyns.log"
    save_lod = "./load.log"
    main(explore, load, save_exp, save_lod)
