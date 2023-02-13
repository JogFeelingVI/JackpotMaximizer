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
        'ins': '^(0[12457])\\s(03|1[134567]|2[012])\\s(09|1[0148]|2[2356])((?!06|08|23|24).)*\\s\\+\\s(0[12789]|1[456])$',
        'n': 50,
        'r': 6,
        'b': 1,
        'jhr': [2, 3, 14, 21, 29, 32],
        'jhb': [8]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()