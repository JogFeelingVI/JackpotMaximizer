# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-14 08:43:47
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-14 09:31:07
from codex import multip_v4



def main():
    print("Hello, World!")
    conf = {'dict':'keys', 'n':150000}
    multip_v4.initialization(conf=conf)
    multip_v4.tasked()


if __name__ == "__main__":
    main()
