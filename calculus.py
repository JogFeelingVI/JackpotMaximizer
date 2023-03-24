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
        'n': 10000,
        'r': 6,
        'b': 1,
        'jhr': [6, 9, 20, 26, 28, 33],
        'jhb': [1]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()