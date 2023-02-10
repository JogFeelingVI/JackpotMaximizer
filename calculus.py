#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-03 15:26:39
from codex import funcs


def test():
    args = {
        'ins': '(.*)',
        'n': 5,
        'r': 6,
        'b': 1,
        'jhr': [8, 10, 14, 15, 18, 22],
        'jhb': [8]
    }
    act = funcs.action(args)
    act.Moni_Calcu()


if __name__ == '__main__':
    test()