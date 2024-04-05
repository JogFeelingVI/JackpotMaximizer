# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-29 23:50:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-04 23:40:24

from codex import funcs_v2
import Insight, time, datetime, threading, pathlib, emoji, sys

ARGS = {
    'dnsr': False, 
    'noinx': False, 'fix': 'a', 'cpu': 'c', 'loadins': True, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 1000, 'r': 6, 'b': 1, 'subcommand': 'load'}
cyns_info = pathlib.Path('cyns.log')
match_cyns = [x for x in range(0, 28)]
result = []
insert_test = []
finished_event = threading.Event()
# insert_test item = (0, [2, 9 ,12, 19, 21, 31], [4])

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
r = lambda s: f'{RED}{s}{ENDC}'
y = lambda s: f'{YELLOW}{s}{ENDC}'
b = lambda s: f'{BLUE}{s}{ENDC}'

def whoistime():
    now = datetime.datetime.now()

# 获取星期几
    weekday =  now.strftime("%A")
    # 转换为中文星期
    weekday_dict = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", 
                    "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", 
                    "Sunday": "星期日"}
    weekday_cn = weekday_dict.get(weekday, "未知")
    # 获取上午或下午
    am_pm = "上午" if now.hour < 12 else "下午"
    # 获取小时数
    hour = now.hour % 12  # 12小时制
    # 格式化时间输出
    return f"{now.year}年{now.month}月{now.day}日 {weekday_cn}, {am_pm} {hour}点"

def main(args:dict = ARGS, mcyns:list = match_cyns):
    print(f'Welcome to the world of wealth. {whoistime()}')
    cyns_index = 0
    while 1:
        global insert_test
        start_time = time.perf_counter()
        # 获得act 传回来的参数
        def m_result(r):
            global result
            print(f'exec callblack {r[0][1]}')
            result = r
        now = funcs_v2.Lastime()
        if insert_test == []:
            act = funcs_v2.action(args, callblack=m_result)
        else:
            m_result(insert_test)
        # print(f'{result[0]}')
        # (0, [9, 12, 16, 17, 31, 33], [8])

        diff_info = Insight.diffMain(show=False, result=result)
        if diff_info == 0:
            continue
        fromid, cyn, n, t = diff_info
        logs = f'{now} -> id {fromid:>4} / cyn {cyn} * {n} + {t}'
        match cyn:
            case Xw if Xw not in mcyns:
                print(f'{b(logs)}')
                # 以追加模式打开文件
            case Bz if Bz == min(mcyns):
                print(f'{r(logs)} {Bz = }')
                with open(cyns_info, "a") as file:
                    # 将信息写入文件
                    file.write(f'{logs}\n')
                    cyns_index += 1
            case Gf if Gf in mcyns:
                print(f'{y(logs)} {Bz = }')
                with open(cyns_info, "a") as file:
                    # 将信息写入文件
                    file.write(f'{logs}\n')
                    cyns_index += 1
            case _:
                print(f'{logs}')
        end_time = time.perf_counter()
        print(f'This running time is {end_time-start_time-3:.4f} seconds')
        if cyns_index >= 3:
            global finished_event
            finished_event.set()
            break
                
def monitor():
    global finished_event
    while True:
        if finished_event.wait(timeout=1):  # 检查主线程是否存活
            print('The workers have gone off work and the monitors are about to take a break.')
            break
        else:
            size = f'{cyns_info.stat().st_size/1024:.2f} kb'
            last_time = datetime.datetime.fromtimestamp(cyns_info.stat().st_mtime)
            print(f'{emoji.emojize(":pulgar_hacia_arriba:", language="es")} The worker is in good condition and has completed `{r(size)}`, working effectively.')
            print(f'Last Modified {r(last_time)}')
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
                    id_str, info = parts[1].split("*")
                    # print(f'{id_str = } {info = }')
                    # return
                    try:
                        id_num = int(id_str.strip())
                        data.append((id_num, info.strip()))
                        # print(f'{id_num = } {info = }')
                        # return 
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
    argvs = ['check','explore']
    
    argv = ''
    if len(sys.argv) > 1:
        argv = sys.argv[1] if sys.argv[1] in argvs else 'explore'
    match argv:
        case 'check':
            extract_and_print_info(cyns_info)
        case 'explore':
            mainx = threading.Thread(target=main, name="workman")
            watcher = threading.Thread(target=monitor, name='watcher', daemon=True)
            mainx.start()
            watcher.start()
            mainx.join()
        case _:
            print(f'Available modes {argvs}')
    
