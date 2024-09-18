#!/usr/bin/env python
# @Author: JogFeelingVi
# @Date: 2022-10-01 18:25:48
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-29 23:42:35
from codex.runingtime import runingtime
from codex.command import loading
from codex.funcs_v2 import action


@runingtime
def main():
    ''' codex enter '''
    cmd_load = loading()
    act = action(cmd_load.gparse())


if __name__ == '__main__':
    main()
