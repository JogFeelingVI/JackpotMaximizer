# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-29 23:50:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-23 15:04:54

from codex import funcs_v2, tonji
import Insight, time, datetime, threading, pathlib, sys, ast, collections

ARGS = {
    'dnsr': False, 
    'noinx': False, 'fix': 'a', 'cpu': 'c', 'loadins': True, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 1000, 'r': 6, 'b': 1, 'subcommand': 'load'}
cyns_info = pathlib.Path('cyns.log')
match_cyns = {4:47.5366, 5:1.4627, 6:0.009}
result = []

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN= "\033[92m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
r = lambda s: f'{RED}{s}{ENDC}'
y = lambda s: f'{YELLOW}{s}{ENDC}'
b = lambda s: f'{BLUE}{s}{ENDC}'
g = lambda s: f'{GREEN}{s}{ENDC}'

def loadLoerLine(path:pathlib.Path):
    with path.open('r') as rlog:
        lines = rlog.readlines()
        if lines.__len__() >= 1:
            return [ast.literal_eval(x) for x in lines]
    return[]

            
def loger(e, name:str):
    now = datetime.datetime.now()
    # 格式化时间为指定的格式
    formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return f'@{name} The error occurred at {formatted_time}, specifically: {e}\n'

def whoistime():
    now = datetime.datetime.now()

# 获取星期几
    weekday =  now.strftime("%A")
    # 转换为中文星期
    weekday_dict = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", 
                    "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", 
                    "Sunday": "星期日"}
    weekday_cn = weekday_dict.get(weekday, "未知")
    # # 获取上午或下午
    # am_pm = "AM" if now.hour < 12 else "PM"
    # 获取小时数
    # hour = now.hour % 12  # 12小时制
    # 格式化时间输出
    # (2024年04月05日 星期五 23时01分51秒)
    return f"{now.year}年{now.month}月{now.day}日 {weekday_cn}, {now.hour}点{now.minute}分{now.second}秒"

def main_rego(args:dict = ARGS):
    start_time = time.perf_counter()
    # 获得act 传回来的参数
    def m_result(r):
        global result
        print(f'exec callblack {r[0][1]}')
        result = r
    now = funcs_v2.Lastime()
    funcs_v2.action(args, callblack=m_result)
    if  result == []:
        print(f'{r("The sample parameters are empty, please adjust the parameters and try again...")}')
        return
    print(f'result len {result.__len__()}')
    diff_info = Insight.diffMain(result=result)
    if diff_info == None:
        return
    with open(cyns_info, "a") as file:
                        # 将信息写入文件
        grouped_arrays = collections.defaultdict(list)
        for array in diff_info:
            third_element = tuple(array[2])
            grouped_arrays[third_element].append(array)
        
        fromid, cyn, n, t = 0, {},[],[]
        for third_element, group in grouped_arrays.items():
            for _g in group:
                _f, _c, _n, _t = _g
                if _n != n:
                    fromid, cyn,n,t = _f,_c,_n,_t
                else:
                    t.extend(_t)
            L456 = sum((cyn.get(4, 0), cyn.get(5, 0), cyn.get(6, 0))) / 10000
            logs = f'{now} -> id {fromid:>4} / cyn {cyn} * {n} + {t}'
            if abs(L456-0.004900) <=0.0002:
                print(f'{r(third_element)} {cyn = }', end='\r')
                file.write(f'{logs}\n')
        print(f'completed 100% {" "* 60}')

def main(tasks:int =100, args:dict = ARGS):
    print(f'Welcome to the world of wealth. {g(whoistime())}')
    try:
        sq = time.perf_counter()
        task = []
        while task.__len__() < tasks:
            start_time = time.perf_counter()
            # 获得act 传回来的参数
            def m_result(r):
                global result
                print(f'exec callblack {r[0][1]}')
                result = r
            now = funcs_v2.Lastime()
            funcs_v2.action(args, callblack=m_result)
            
            if  result == []:
                print(f'{r("The sample parameters are empty, please adjust the parameters and try again...")}')
                return
            print(f'result len {result.__len__()}')
            diff_info = Insight.diffMain(result=result)
            if diff_info == None:
                continue
            # ???
            echo = False
            with open(cyns_info, "a") as file:
                for item in diff_info.copy():
                    fromid, cyn, n, t = item
                    logs = f'{now} -> id {fromid:>4} / cyn {cyn} * {n} + {t}'
                    L456 = sum((cyn.get(4, 0), cyn.get(5, 0), cyn.get(6, 0))) / 10000
                    if abs(L456-0.004900) <= 0.0002:
                        task.append(item)
                        if echo == False:
                            print(f'{r(logs)}')
                            echo = True
            # ???
            end_time = time.perf_counter()
            print(f'This running time is {g(f"{end_time-start_time-3:.4f}")} seconds. {task.__len__()}')
        # task done 
        print(f'task {tasks} is done.')
        grouped_arrays = collections.defaultdict(list)
        for array in task:
            third_element = tuple(array[2])
            grouped_arrays[third_element].append(array)
        
        fromid, cyn, n, t = 0, {},[],[]
        with open(cyns_info, "a") as file:
            for third_element, group in grouped_arrays.items():
                for _g in group:
                    _f, _c, _n, _t = _g
                    if _n != n:
                        fromid, cyn,n,t = _f,_c,_n,_t
                    else:
                        _t = [x for x in _t if x not in t]
                        t.extend(_t)
                
                logs = f'{now} -> id {fromid:>4} / cyn {cyn} * {n} + {t}'
                print(f'{r(third_element)} {cyn = }', end='\r')
                file.write(f'{logs}\n')
                
        print(f'completed 100% {" "*10} {time.perf_counter() - sq:.4f} seconds.')
        
    except Exception as e:
        print(f'ERR: {e}')
        with open('error.log', "a") as file:
            # 将信息写入文件
            file.write(loger(e, 'Jpm_insight -> main'))
        
def loadLine(path:pathlib.Path):
    print(f'Welcome to the world of wealth. {g(whoistime())}')
    try:
        start_time = time.perf_counter()
        insert_test = loadLoerLine(path)
        if insert_test == []:
            print(f'{r("The sample parameters are empty, please adjust the parameters and try again...")}')
            return
        diff_info = Insight.diffMain(result=insert_test)
        if diff_info != None:
            for item in diff_info:
                print(f'{item}')
        end_time = time.perf_counter()
        print(f'This running time is {g(f"{end_time-start_time-3:.4f}")} seconds. {insert_test.__len__()}')
            
    except Exception as e:
        print(f'ERR: {e}')
        with open('error.log', "a") as file:
            # 将信息写入文件
            file.write(loger(e, 'Jpm_insight -> loadLine'))
            
def tongji(path:pathlib.Path):
    print(f'Welcome to the world of wealth. {g(whoistime())}')
    try:
        start_time = time.perf_counter()
        insert_test = loadLoerLine(path)
        tjone = tonji.statistics()
        tjone.Statistical_length = 5
        count_id = 1
        for id, r, b in insert_test:
            n = tonji.sublist(count_id, r, b)
            tjone.add(n)
            count_id += 1
        print(f'====== {time.time()} ======')
        vid = []
        for k, v in  tjone.same_numbers_dict.items():
            print(f'key {k} len {len(v)} value {v}')
            if len(v) in [3,1,2]:
                [vid.append(x) for x in v if x not in vid]
        info = f' lens {tjone.same_numbers_dict.keys().__len__()}/{vid.__len__()} '
        print(f'{ info :+^70}')
        for i, item in enumerate(insert_test):
            _, r, b = item
            if i+1 in vid:
                print(f'{i+1} / {r} + {b}')
        # filter_data = sq3.read_data_by_ids(vid)
        # if filter_data != None:
        #     for fItem in filter_data:
        #         id, r, b = fItem
        #         print(f'id: {id:>3} / {r} + {b}')
        # else:
        #     print('No data matching the filter criteria.')
        end_time = time.perf_counter()
        print(f'This running time is {g(f"{end_time-start_time:.4f}")} seconds. {insert_test.__len__()}')
    except Exception as e:
        print(f'ERR: {e}')
        with open('error.log', "a") as file:
            # 将信息写入文件
            file.write(loger(e, 'Jpm_insight -> tongji'))
        
                
def monitor(tasks:list, finished_event:threading.Event):
    while True:
        if not tasks and finished_event.is_set():
            print('The workers have gone off work and the monitors are about to take a break.')
            break
        else:
            size = f'{cyns_info.stat().st_size/1024:.2f} kb'
            last_time = datetime.datetime.fromtimestamp(cyns_info.stat().st_mtime)
            print(f'The worker is in good condition and has completed `{r(size)}`, working effectively. Last Modified {r(last_time)}. Tasks {tasks.__len__()}')
        time.sleep(30)
        

def extract_and_print_info(file_path):
    """
    从文件中提取 id 信息，排序并打印。

    Args:
        file_path (str): 文件路径。
    """

    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()  # 去除首尾空格
            if line:  # 检查是否为空行
                parts = line.split("/ cyn")
                # print(f'{parts = }')
                # # parts = ['@Last Modified time: 2024-04-04 09:36:32 -> id  930 ', ' 26 * [4, 9, 13, 18, 24, 32] + [13]']
                # return
                if len(parts) == 2:
                    # 提取 id 和信息
                    cyns, info = parts[1].split("*")
                    # print(f'{id_str = } {info = }')
                    # return
                    try:
                        cyns = int(cyns.strip())
                        r, b = info.split('+')
                        r= ' '.join((f'{x:02}' for x in ast.literal_eval(r)))
                        b = ' '.join((f'{x:02}' for x in ast.literal_eval(b)))
                        data.append((cyns, f' ➤ {r} ⎯ {b}'))
                    except ValueError:
                        print(f"Invalid row: {line}")
    # 排序
    data.sort(key=lambda item: item[0])
    count = 0
    # 打印信息，每行后添加空行
    for item in data[0:20]:
        id, info = item
        print(f'{id} * {info}')
        count +=1 
        if count == 5:
            print()
            count = 0

            
if __name__ == "__main__":
    argvs = ['check','explore', 'load']
    print(f'{sys.argv = }')
    match sys.argv:
        case [_, 'check']:
            print(f'{g("Use `check` to execute the program")}')
            extract_and_print_info(cyns_info)
        case [_,'explore']:
            print(f'{g("Use `explore` to execute the program")}')
            tasks = 200
            main(tasks=tasks)
        case [_, 'explore', 'rego']:
            ARGS.update({'cpu':'d'})
            print(f'{g("Use `explore` to execute the program")} CPU = rego ')
            main_rego()
        case [_, 'load', path]:
            print(f'{g(f"Use `Load {path}` to execute the program")}')
            if (p:=pathlib.Path(path)).exists():
                loadLine(p)
            else:
                print(f'Use `load` to start the program, but the `{path}` file does not exist.')
        case [_, 'tongji', path]:
            print(f'{g(f"Use `Load {path}` to execute the program")}')
            if (p:=pathlib.Path(path)).exists():
                tongji(p)
            else:
                print(f'Use `load` to start the program, but the `{path}` file does not exist.')
        case [_, 'load']:
            print(f'{r("To start a program using `load`, the specified file must be provided.")}')
            print(f'{r("For example `poetry run python3 ./jpm_insight.py load ./outing_id_r_b.log`")}')
        case _:
            print(f'Available modes {argvs}')
    
