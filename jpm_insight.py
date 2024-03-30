# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-29 23:50:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-30 18:43:37

from codex import funcs_v2
import Insight, time

cyns_info = 'cyns.log'
result = []

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"  # 重置颜色

# 打印彩色字符
r = lambda s: f'{RED}{s}{ENDC}'
y = lambda s: f'{YELLOW}{s}{ENDC}'
b = lambda s: f'{BLUE}{s}{ENDC}'

def main():
    print("Hello, World!")
    args = args_c = {'dnsr': False, 'noinx': False, 'fix': 'a', 'cpu': 'c', 'loadins': False, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 1000, 'r': 6, 'b': 1, 'subcommand': 'load'}
    cyns_index = 0
    while 1:
        start_time = time.perf_counter()
        # 获得act 传回来的参数
        def m_result(r):
            global result
            print(f'exec callblack {r[0]}')
            result = r
        now = funcs_v2.Lastime()
        act = funcs_v2.action(args, callblack=m_result)
        # print(f'{result[0]}')
        # (0, [9, 12, 16, 17, 31, 33], [8])

        diff_info = Insight.diffMain(show=False, result=result)
        fromid, cyn, n, t = diff_info
        logs = f'{now} -> id {fromid:>4} / cyn {cyn} * {n} + {t}'
        match cyn:
            case Xw if Xw <= 25:
                print(f'{b(logs)}')
                # 以追加模式打开文件
            case Bz if Bz <=4:
                print(f'{r(logs)} {Bz = }')
                with open(cyns_info, "a") as file:
                    # 将信息写入文件
                    file.writelines(logs)
                    cyns_index += 1
            case Jp if Jp <= 16:
                print(f'{y(logs)} {Jp = }')
                with open(cyns_info, "a") as file:
                    # 将信息写入文件
                    file.writelines(logs)
                    cyns_index += 1
            case _:
                print(f'{logs}')
        end_time = time.perf_counter()
        print(f'This running time is {end_time-start_time-3:.4f} seconds')
        if cyns_index >=5:
            break
                

            
if __name__ == "__main__":
    main()
