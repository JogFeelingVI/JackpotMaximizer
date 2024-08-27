# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-03 09:22:28
# @Last Modified by:   Your name
# @Last Modified time: 2024-08-28 00:01:03


import time, json, pathlib, pytest
from typing import List
from codex import funcs_v2
from codex.runingtime import runingtime


def test_get_number():
    print("kaishi test")
    args = {
        "dnsr": True,
        "noinx": False,
        "fix": "a",
        "cpu": "a",
        "loadins": False,
        "usew": "s",
        "debug": False,
        "ins": "(.*)",
        "n": 25,
        "r": 6,
        "b": 1,
        "subcommand": "load",
    }
    act = funcs_v2.action(args=args)


if __name__ == "__main__":
    test_get_number()
