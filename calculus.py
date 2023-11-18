#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-17 06:07:18
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
        'n': 1000,
        'r': 6,
        'b': 1,
        'jhr': [4, 10, 17, 22, 23, 32],
        'jhb': [16]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()
