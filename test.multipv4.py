# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-14 08:43:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-15 20:35:59
from codex import multip_v4


def main():
    print("Hello, World!")
    conf = {"n": 10000, "loadins": False, "loadfilter": False}
    p = multip_v4
    p.initialization(conf=conf)
    print(f'{p.config}')
    Retds = p.tasked()


if __name__ == "__main__":
    main()
