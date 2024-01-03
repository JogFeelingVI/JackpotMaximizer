# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2023-12-26 20:55:18
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-03 15:47:04

from typing import List
from functools import partial
import pathlib, re
from codex import ospath

from codex import note

filenam = ospath.findAbsp.file_path('insx.rego')


def load_rego_v2() -> str:
    '''装载rego文件'''
    rego = pathlib.Path(filenam)
    with rego.open(mode='r', encoding='utf-8') as go:
        return go.read()


# class Note:

#     def __init__(self) -> None:
#         self.number = []
#         self.tiebie = []
#         self.setnumber_R = set()
#         self.setnumber_B = set()

#     def index(self, i=1):
#         return 1


class Lexer:

    def __init__(self, debug='') -> None:
        self.debug = debug
        self.rules = [
            #(re.compile(r'^#.*$'), self.handle_comment),
            (re.compile(r'^- [ 0-9]+as (R|B)$'), self.handle_paichu),
            (re.compile(r'^\+ [ 0-9]+as R$'), self.handle_baohan),
            (re.compile(r'^\+ [ 0-9]+ (@bit[1-7])$'), self.handle_bit),
            (re.compile(r'^- [ 0-9]+ (@bit[1-7])$'), self.handle_bitex),
        ]

    def pares(self, rego: str):
        '''词法分析'''
        result = {}
        index = 1
        for line in rego.splitlines():
            for pattern, handler in self.rules:
                match = pattern.match(line)
                if match:
                    result.update({index: handler(match=match)})
                    index += 1
                    break
        return result

    def handle_paichu(self, match):
        match_list = match.group(0).split()
        numbers = [int(x) for x in match_list[1:-2]]
        rb = match.group(1)
        if self.debug.count('v') == 1:
            print(f'debug paichu {match.group(0)} | {numbers} ? {rb}')
        match rb:
            case 'R':
                return partial(rego_filter.f_paichu_r, args=numbers)
            case 'B':
                return partial(rego_filter.f_paichu_b, args=numbers)
            case _:
                return {}

    def handle_baohan(self, match):
        match_list = match.group(0).split()
        numbers = [int(x) for x in match_list[1:-2]]
        partial_func = partial(rego_filter.f_baohan, args=numbers)
        if self.debug.count('v') == 1:
            print(f'debug baohan {match.group(0)} | {numbers}')
        return partial_func

    def handle_bit(self, match):
        match_list = match.group(0).split()
        numbers = [int(x) for x in match_list[1:-1]]
        bit = int(match.group(1)[-1])
        partial_func = partial(rego_filter.f_bit, args=numbers, index=bit)
        if self.debug.count('v') == 1:
            print(f'debug bit {match.group(0)} | {numbers} ? {bit}')
        return partial_func

    def handle_bitex(self, match):
        match_list = match.group(0).split()
        numbers = [int(x) for x in match_list[1:-1]]
        bit = int(match.group(1)[-1])
        partial_func = partial(rego_filter.f_bitex, args=numbers, index=bit)
        if self.debug.count('v') == 1:
            print(f'debug bit {match.group(0)} | {numbers} ? {bit}')
        return partial_func

    def handle_comment(self, match):
        '''注释'''
        print(f'debug zhushi {match.group()}')
        return {}


class rego_filter:

    @staticmethod
    def f_paichu_r(N: note.Note, args: List) -> bool:
        '''排除'''
        for _n in N.number:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_paichu_b(N: note.Note, args: List) -> bool:
        '''排除'''
        for _n in N.tiebie:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_baohan(N: note.Note, args: List) -> bool:
        '''包含'''
        for _n in N.setnumber_R:
            if _n in args:
                return True
        return False

    @staticmethod
    def f_bit(N: note.Note, args: List, index: int) -> bool:
        '''定位 包含'''
        match index:
            case 1 | 2 | 3 | 4 | 5 | 6:
                _n = [N.index(i=index)]
            case 7:
                _n = N.tiebie
            case _:
                _n = [0]
        if len(set(_n) & set(args)) == 0:
            return False
        return True

    @staticmethod
    def f_bitex(N: note.Note, args: List, index: int) -> bool:
        '''定位 不包含'''
        match index:
            case 1 | 2 | 3 | 4 | 5 | 6:
                _n = [N.index(i=index)]
            case 7:
                _n = N.tiebie
            case _:
                _n = [0]
        if len(set(_n) & set(args)) > 0:
            return False
        return True


def main():
    print("Hello, World!")
    rego = load_rego_v2()
    lexer = Lexer(debug='v')
    result = lexer.pares(rego=rego)
    print(f'ok {result}')


if __name__ == "__main__":
    main()
