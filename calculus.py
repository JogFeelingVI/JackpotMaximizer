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
        'loadins': True,
        'ins': '(.*)',
        'n': 100,
        'r': 6,
        'b': 1,
        'jhr': [14, 16, 19, 23, 28, 30],
        'jhb': [3]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()