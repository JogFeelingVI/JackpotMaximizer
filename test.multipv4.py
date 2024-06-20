# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-14 08:43:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-20 12:29:01
from codex import multip_v4


def main():
    print("Hello, World!")
    conf = {"n": 1000000, "loadins": True, "loadfilter": True}
    p = multip_v4
    p.initialization(conf=conf)
    Retds = p.tasked()


if __name__ == "__main__":
    main()
