#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-15 14:14:30
from codex import funcs_v2
from codex.runingtime import runingtime


@runingtime
def Moni_T():
    args = {
        "subcommand": "simulation",
        "debug": False,
        "dnsr": False,
        "noinx": False,
        "loadins": False,
        # "usew": "s",
        # "fix": "a",
        "cpu": "m",
        "ins": "(.*)",
        "n": 100000,
        "r": 6,
        "b": 1,
        "Compared-R": [1, 7, 10, 16, 18,27],
        "Compared-B": [16],
    }
    act = funcs_v2.action(args)


if __name__ == "__main__":
    Moni_T()
