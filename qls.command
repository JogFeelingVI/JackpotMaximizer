#!/usr/bin/env python3
# @Author: JogFeelingVi
# @Date: 2022-10-01 18:25:48
# @Last Modified by:   By JogFeelingVi
# @Last Modified time: 2022-10-01 18:25:48

import argparse
from codex import loadjson

if __name__ == '__main__':
    Ljson = loadjson.Load_JSON()
    print(Ljson.read('command_info'))
    
