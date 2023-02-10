#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39
from codex import funcs


def test():
    args = {
        'ins': '^(06)\\s(07)((?!22|24|11|16|17|28|33).)*$',
        'n': 1000,
        'r': 6,
        'b': 1,
        'jhr': [6, 7, 18, 23, 27, 30],
        'jhb': [5]
    }
    act = funcs.action(args)
    for x in range(10):
        act.Moni_Calcu()


if __name__ == '__main__':
    test()