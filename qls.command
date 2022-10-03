#!/usr/bin/env python3
# @Author: JogFeelingVi
# @Date: 2022-10-01 18:25:48
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-01 18:25:48

import argparse
from codex.loadjson import Load_JSON, Resty
from codex.command import loading


def maix() -> None:
    ''' codex enter '''
    Ljson = Load_JSON(Resty.OxStr)
    Cmd_load = loading()
    print(Cmd_load.gparse())


if __name__ == '__main__':
    maix()
