# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-30 07:04:55
# @Last Modified by:   Your name
# @Last Modified time: 2024-09-10 17:48:09
from codex import multip_v4
import time, datetime, threading, pathlib, sys, ast, collections, re

ARGS = {"n": 1000, "loadins": True, "loadfilter": True}

cyns_info = pathlib.Path("cyns.log")
match_cyns = {4: 47, 5: 1.5, 6: 0}
result = []

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
r = lambda s: f"{RED}{s}{ENDC}"
y = lambda s: f"{YELLOW}{s}{ENDC}"
b = lambda s: f"{BLUE}{s}{ENDC}"
g = lambda s: f"{GREEN}{s}{ENDC}"


def Lastime() -> str:
    """
    @Last Modified time: 2023-11-21 10:32:45
    """
    now = datetime.datetime.now()
    # 格式化时间字符串
    formatted_time = now.strftime("@Last Modified time: %Y-%m-%d %H:%M:%S")
    return formatted_time


def explore_task(task: int = 25):
    tasks = []
    while tasks.__len__() < task:
        Start_Time = Lastime()
        p = multip_v4
        p.initialization(conf=ARGS)
        Retds = p.tasked()
        if Retds:
            tasks.extend([1] * Retds.__len__()) 
            with open(cyns_info, "a") as file:
                for rdx in Retds:
                    fromid, n, t, dfr4, dfr5 = rdx
                    cyns = {4:dfr4, 5:dfr5}
                    logs = (
                        f"{Start_Time} -> id {fromid:>4} / cyn {cyns} * {n} + {t}"
                    )
                    print(f"Logs: {logs}")
                    file.write(f"{logs}\n")
                    time.sleep(1)


def load_cynslog(path:pathlib.Path):
    # cyns_json = pathlib.Path(path)
    search_id_cyn_r_b = re.compile(r"id\s+(\d+).*\{(.*)\}\s\*\s(.*)\s\+\s(.*)")
    idex_range = [f"{x:02}" for x in range(1, 10000)]
    data = []
    with path.open("r+") as f:
        for line in f:
            line = line.strip()  # 去除首尾空格
            if line:  # 检查是否为空行
                match_search = search_id_cyn_r_b.search(line)
                if match_search == None:
                    return data
                _id, cyns, _r, _b = match_search.groups()
                _cyns = ast.literal_eval(f"{{{cyns}}}")
                _id = idex_range[0]
                idex_range.remove(_id)
                data.append({"red": ast.literal_eval(_r), "bule": ast.literal_eval(_b), "id":_id, "logs":0})
    # cyns_json.unlink()
    # 排序
    return data


def load_task(task:int=20):
    cyns_json = pathlib.Path("./cyns.log")
    cyns_data = load_cynslog(cyns_json)
    Start_Time = Lastime()
    def recyns(p:str):
        return cyns_data
    p = multip_v4
    p.initialization(conf=ARGS)
    tasks = [0] * task
    while tasks.count(0) != 0:
        Retds = p.loadtask(loadlog=recyns)
        if Retds:
            for rix in Retds:
                find_id = dict(rix).get('id', '')
                for cd in cyns_data:
                    if cd['id'] == find_id:
                        cd['logs'] += 1
        index = tasks.index(0)
        tasks[index] = 1
    print(f'{r("Mission completed, sorting in progress.")}')
    data = sorted(cyns_data, key=lambda item: item['logs'], reverse=True)
    info = f'#\n# The differ program has been executed, the task\n# parameter is {task}, and the execution results are as\n# follows: data lens {len(data)}\n#\n'
    with open(cyns_info, "w") as file:
        file.write(f"{info}\n")
        for _da in data:
            # {'red': [6, 7, 13, 20, 25, 29], 'bule': [16], 'id': '05', 'logs': 8, 'DFR4': 48, 'DFR5': 0}
            _r, _b, _id, logs, *_ = _da.values()
            n = f'{_r}'
            t = f'{_b}'
            cyns = {4:logs}
            logstr = f"{Start_Time} -> id {_id:>4} / logs {cyns} * {n} + {t}"
            print(f'{logstr = }')
            file.write(f'{logstr}\n')
            time.sleep(1)
        


if __name__ == "__main__":
    argvs = ["check", "explore", "load"]
    print(f"{sys.argv = }")
    match sys.argv:
        case [_, "check"]:
            print(f"runting check...")
        case [_, "explore", "task", task_args]:
            print(f"runting explore -> task {task_args}")
            explore_task(task=int(task_args))
        case [_, "load", "task", task_args ]:
            print(f"runting loader -> task {task_args}")
            load_task(task=int(task_args))
