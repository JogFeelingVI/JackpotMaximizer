#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-20 07:35:18
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
        'Compared-R': [4, 6, 7, 14, 15, 24],
        'Compared-B': [8]
    }
    act = funcs_v2.action(args)

if __name__ == '__main__':
    Moni_T()
