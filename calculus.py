#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-03 15:26:39
# @Last Modified by:   Your name
# @Last Modified time: 2024-08-28 00:03:51
from codex import funcs_v2
from codex.runingtime import runingtime


@runingtime
def Moni_T():
    args = {
        "dnsr": True,
        "noinx": False,
        "fix": "a",
        "cpu": "a",
        "loadins": False,
        "usew": "s",
        "debug": False,
        "ins": "(.*)",
        "n": 1000,
        "r": 6,
        "b": 1,
        "subcommand": "load",
        "Compared-R": [1, 7, 10, 16, 18, 27],
        "Compared-B": [16],
    }
    act = funcs_v2.action(args)


if __name__ == "__main__":
    Moni_T()
