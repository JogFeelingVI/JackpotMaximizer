# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-03 09:22:28
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-03 17:57:25


import time, json, pathlib,pytest
from typing import List
from codex.funcs import action


def test_get_number():
    print('kaishi test')
    args = {
        'save':False,
        'noinx':False,
        'debug': False,
        'loadins': True,
        'usew': 'c',
        'fix': 'a',
        'cpu': 'a',
        'ins': '(.*)',
        'n': 25,
        'r': 6,
        'b': 1,
        'subcommand': 'load',
    }
    act = action(args=args)
    act.act_for_dict()
