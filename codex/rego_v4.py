# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2023-12-26 20:55:18
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-14 07:46:25

from typing import List
from functools import partial
import pathlib, re, itertools
from codex import ospath
from dataclasses import dataclass

filenam = ospath.findAbsp.file_path('insx.rego')


def load_rego_v2() -> str:
    '''装载rego文件'''
    rego = pathlib.Path(filenam)
    with rego.open(mode='r', encoding='utf-8') as go:
        return go.read()

@dataclass
class range_itertools:
    ranges = dict.fromkeys(range(1, 8),[x for x in range(1, 34)])
    
    def product(self):
        '''from key product all list'''
        keys = sorted(self.ranges.keys())
        range_p = itertools.product(*[self.ranges[key] for key in keys])
        return range_p

    def add(self, bitx:int, number_list:List[int]):
        '''
        bitx 1 2 3 4 5 6 7
        number_list [1,2,3,4...33]
        '''
        self.ranges[bitx] = number_list

class Lexer:
    range_product = range_itertools()

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
        return result, self.range_product

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
        self.range_product.add(bit, numbers)
        partial_func = partial(rego_filter.f_bit, args=numbers, index=bit)
        if self.debug.count('v') == 1:
            print(f'debug bit {match.group(0)} | {numbers} ? {bit}')
        return partial_func

    def handle_bitex(self, match):
        match_list = match.group(0).split()
        numbers = [int(x) for x in match_list[1:-1]]
        bit = int(match.group(1)[-1])
        self.range_product.add(bit, [x for x in range(1, 34) if x not in numbers])
        partial_func = partial(rego_filter.f_bitex, args=numbers, index=bit)
        if self.debug.count('v') == 1:
            print(f'debug bit {match.group(0)} | {numbers} ? {bit}')
        return partial_func

    def handle_comment(self, match):
        '''注释'''
        print(f'debug zhushi {match.group()}')
        return {}


class rego_filter:
    '''
    data {'red': [2, 4, 8, 16, 24, 33], 'bule': [10]}
    '''

    @staticmethod
    def f_paichu_r(n:list, args: List) -> bool:
        '''排除'''
        for _n in n:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_paichu_b(n:list, args: List) -> bool:
        '''排除'''
        for _n in n:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_baohan(n:list, args: List) -> bool:
        '''包含'''
        for _n in n:
            if _n in args:
                return True
        return False

    @staticmethod
    def f_bit(n:list, args: List, index: int) -> bool:
        '''定位 包含'''
        match index:
            case 1 | 2 | 3 | 4 | 5 | 6:
                _n = [n[index-1]]
            case 7:
                _n = n
            case _:
                _n = [0]
        if len(set(_n) & set(args)) == 0:
            return False
        return True

    @staticmethod
    def f_bitex(n:list, args: List, index: int) -> bool:
        '''定位 不包含'''
        match index:
            case 1 | 2 | 3 | 4 | 5 | 6:
                _n = [n[index-1]]
            case 7:
                _n = n
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
