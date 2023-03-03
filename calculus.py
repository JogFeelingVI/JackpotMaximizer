#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39
from codex import funcs
from codex.runingtime import runingtime


@runingtime
def Moni_T():
    args = {
        'debug': True,
        'loadins': True,
        'fix': 'a',
        'cpu': 'm',
        'ins': '(.*)',
        'n': 3000,
        'r': 6,
        'b': 1,
        'jhr': [5, 8, 10, 15, 24, 25],
        'jhb': [9]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()