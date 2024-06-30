# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-30 07:04:55
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-30 15:04:26
from codex import multip_v4
import time, datetime, threading, pathlib, sys, ast, collections

ARGS = {"n": 1000, "loadins": True, "loadfilter": True}

cyns_info = pathlib.Path("cyns.log")
match_cyns = {4: 47.5366, 5: 1.4627, 6: 0.009}
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
    tasks = [0] * task
    while tasks.count(0) != 0:
        Start_Time = Lastime()
        p = multip_v4
        p.initialization(conf=ARGS)
        Retds = p.tasked()
        if Retds:
            index = tasks.index(0)
            tasks[index] = 1
            with open(cyns_info, "a") as file:
                for rdx in Retds:
                    fromid, n, t = rdx
                    logs = (
                        f"{Start_Time} -> id {fromid:>4} / cyn {match_cyns} * {n} + {t}"
                    )
                    print(f"Logs: {logs}")
                    file.write(f"{logs}\n")
                    time.sleep(1)


if __name__ == "__main__":
    argvs = ["check", "explore", "load"]
    print(f"{sys.argv = }")
    match sys.argv:
        case [_, "check"]:
            print(f"runting check...")
        case [_, "explore", "task", task_args]:
            print(f"runting explore -> task -> {task_args}")
            explore_task(task=int(task_args))
