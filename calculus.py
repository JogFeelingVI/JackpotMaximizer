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
        'debug': False,
        'loadins': True,
        'usew': False,
        'fix': 'a',
        'cpu': 'm',
        'ins': '(.*)',
        'n': 10000,
        'r': 6,
        'b': 1,
        'jhr': [8,23,25,26,29,31],
        'jhb': [12]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()