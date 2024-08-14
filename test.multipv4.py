# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-06-14 08:43:47
# @Last Modified by:   Your name
# @Last Modified time: 2024-08-14 10:40:44
from codex import multip_v4


def main():
    print("Hello, World!")
    conf = {"n": 1000000, "loadins": True, "loadfilter": True}
    p = multip_v4
    p.initialization(conf=conf)
    Retds = p.tasked()
    
def test_idex():
    idex_range = []
    index = 1
    while True:
        try:
            _id = idex_range.pop(0)
        except IndexError:
            idex_range.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
            _id = idex_range.pop(0)
            
        print(f'debug {index} { _id} {len(idex_range)= }')
        index+=1
        if index>30:
            break


if __name__ == "__main__":
    test_idex()
