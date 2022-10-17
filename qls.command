#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-01 18:25:48
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-01 18:25:48

from codex.command import loading
from codex.funcs import action


def maix() -> None:
    ''' codex enter '''
    cmd_load = loading()
    act = action(cmd_load.gparse())
    act.act_for_dict()

if __name__ == '__main__':
    maix()
