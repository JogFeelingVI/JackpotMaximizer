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
        'ins':
        '^(0[1248])\\s(0[368]|1[14578]|2[014])\\s(1[12569]|2[35])\\s(1[29]|2[056])\\s(1[47]|2[02489]|3[012])\\s(2[87]|32)\\s\\+\\s(0[27]|1[01])$',
        'n': 5000,
        'r': 6,
        'b': 1,
        'jhr': [14, 16, 19, 23, 28, 30],
        'jhb': [3]
    }
    act = funcs.action(args, diff=True)
    act.Moni_Calcu()


if __name__ == '__main__':
    Moni_T()