#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-29 23:38:12
from codex import funcs_v2
from codex.runingtime import runingtime


@runingtime
def Moni_T():
    args = {
        'subcommand': 'simulation',
        'debug': False,
        'dnsr': False,
        'noinx': False,
        'loadins': True,
        'usew': 's',
        'fix': 'a',
        'cpu': 'm',
        'ins': '(.*)',
        'n': 1000,
        'r': 6,
        'b': 1,
        'Compared-R': [2, 9, 12, 19, 21, 31],
        'Compared-B': [4]
    }
    act = funcs_v2.action(args)

if __name__ == '__main__':
    Moni_T()
