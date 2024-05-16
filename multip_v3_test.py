# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-03 09:32:40
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-09 16:04:04


from codex import multip_v3


def main():
    '''
    (args, data, core, sq3)
    '''
    args = {'dnsr': True, 'noinx': True, 'fix': 'a', 'cpu': 'a', 'loadins': True, 'usew': 's', 'debug': False, 'ins': '(.*)', 'n': 100, 'r': 6, 'b': 1, 'subcommand': 'load'}
    data = {'R': [5, 11, 12, 16, 17, 20, 3, 8, 12, 14, 17, 33, 4, 6, 16, 17, 23, 24, 2, 9, 11, 14, 18, 26, 1, 10, 22, 25, 28, 32, 3, 7, 21, 24, 26, 30, 8, 15, 21, 22, 25, 33, 4, 7, 18, 19, 20, 25, 2, 6, 13, 27, 28, 32, 3, 7, 8, 11, 18, 19, 12, 18, 23, 25, 28, 33, 1, 8, 22, 25, 29, 33, 9, 10, 13, 25, 30, 32, 1, 3, 4, 11, 12, 21, 6, 10, 11, 18, 20, 32, 2, 9, 12, 19, 21, 31, 5, 7, 14, 17, 22, 32, 2, 8, 9, 12, 21, 31, 1, 4, 5, 6, 12, 14, 8, 10, 18, 23, 27, 31, 2, 6, 12, 29, 30, 31, 11, 14, 18, 19, 23, 26, 2, 9, 12, 22, 25, 33, 2, 4, 5, 14, 26, 32, 4, 6, 7, 14, 15, 24, 2, 6, 17, 25, 32, 33, 2, 8, 19, 23, 24, 26, 2, 6, 10, 11, 17, 29, 7, 8, 21, 26, 29, 30, 2, 9, 15, 19, 26, 28], 'B': [8, 8, 11, 6, 10, 10, 13, 6, 13, 5, 4, 10, 2, 16, 5, 4, 6, 2, 13, 2, 10, 2, 16, 14, 8, 6, 3, 15, 15, 2], 'date': '2024-05-02 17:17:23.905004'}
    core= True 
    sq3 = False
    print("Hello, World!")
    match args:
            case {
                "n": int() as n,
                "loadins": bool() as loadins,
                "r": int() as r,
                "b": int() as b,
                "ins": str() as ins,
                "usew": str() as usew,
            }:
                p = multip_v3
                p.settingLength(n)
                p.useRego(loadins)
                p.initPostCall(data, r, b, ins, usew)
                # Retds = p.tasks_single()
                Retds = p.tasks_futures_press()
                # Retds = p.tasks_futures()
            case _:
                pass
    print(f'{Retds = }')


if __name__ == "__main__":
    main()