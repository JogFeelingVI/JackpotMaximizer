#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-01 18:25:48
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-28 21:34:51
from codex.runingtime import runingtime
from codex.command import loading
from codex.funcs import action
import asyncio


@runingtime
def main():
    ''' codex enter '''
    cmd_load = loading()
    act = action(cmd_load.gparse())
    act.act_for_dict()


if __name__ == '__main__':
    main()
