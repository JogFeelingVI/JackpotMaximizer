#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-01 22:58:00
from codex import funcs
from codex.runingtime import runingtime


@runingtime
def Moni_T():
    args = {
        'debug': False,
        'loadins': True,
        'usew': 'c',
        'fix': 'a',
        'cpu': 'm',
        'ins': '(.*)',
        'n': 1000,
        'r': 6,
        'b': 1,
        'jhr': [1, 15, 16, 20, 25, 27],
        'jhb': [5]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()
