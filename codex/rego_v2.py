# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-10-24 19:04:50
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-30 09:51:27

import re, time, pathlib
from typing import List

from codex.glns_v2 import Note

filenam = 'insx.reg'


class rego:
    '''读取rego文件并对列表进行解析'''
    __debug = False

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool) -> bool:
        self.__debug = value
        return self.__debug

    def __init__(self) -> None:
        self.parse_v2(self.load_rego_v2())
        # self.Func = {
        #     'paichu_r': self.f_paichu_r,
        #     'paichu_b': self.f_paichu_b,
        #     'baohan': self.f_baohan,
        #     'bit_1': self.f_bit_1,
        #     'bit_2': self.f_bit_2,
        #     'bit_3': self.f_bit_3,
        #     'bit_4': self.f_bit_4,
        #     'bit_5': self.f_bit_5,
        #     'bit_6': self.f_bit_6,
        #     'bit_7': self.f_bit_7,
        #     'bitex_1': self.f_bitex_1,
        #     'bitex_2': self.f_bitex_2,
        #     'bitex_3': self.f_bitex_3,
        #     'bitex_4': self.f_bitex_4,
        #     'bitex_5': self.f_bitex_5,
        #     'bitex_6': self.f_bitex_6,
        #     'bitex_7': self.f_bitex_7,
        # }

    def load_rego_v2(self) -> str:
        '''装载rego文件'''
        rego = pathlib.Path(filenam)
        with rego.open(mode='r', encoding='utf-8') as go:
            return go.read()

    def p_paichu(self, line: str) -> List | None:
        '''排除法检测'''
        temp = []
        _paichu = re.compile(r'^-[ 0-9]+as [R|B]$', flags=re.M)
        if (_match := _paichu.findall(line)) != None:
            for _m in _match:
                _n = re.compile('[0-9]{1,2}')
                _p = re.compile('R|B')
                rb = _p.findall(_m)
                nm = [int(x, base=10) for x in _n.findall(_m)]
                if 'R' in rb:
                    temp.append({'f': rego_filter.f_paichu_r, 'a': nm})
                if 'B' in rb:
                    temp.append({'f': rego_filter.f_paichu_b, 'a': nm})
            return temp
        return None

    def p_baohan(self, line: str) -> List | None:
        _baohan = re.compile(r'^\+[ 0-9]+as R$', flags=re.M)
        temp = []
        if (_match := _baohan.findall(line)) != None:
            for _m in _match:
                _n = re.compile('[0-9]{1,2}')
                nm = [int(x, base=10) for x in _n.findall(_m)]
                temp.append({'f': rego_filter.f_baohan, 'a': nm})
            return temp
        return None

    def p_bit(self, line: str) -> List | None:
        '''Bit'''
        temp = []
        _bit = re.compile(r'^\+[ 0-9]+@bit[1-7]$', re.M)
        if (_match := _bit.findall(line)) != None:
            for _m in _match:
                _n = re.compile(r'\s([0-9]{1,2})')
                p = re.compile(r'@bit([1-7])$').findall(_m)[0]
                nm = [int(x, base=10) for x in _n.findall(_m)]
                funx = getattr(rego_filter, f'f_bit_{p}')
                temp.append({'f': funx, 'a': nm})
            return temp
        return None

    def p_bitex(self, line: str) -> List | None:
        '''Bit ex'''
        temp = []
        _bit = re.compile(r'^-[ 0-9]+@bit[1-7]$', re.M)
        if (_match := _bit.findall(line)) != None:
            for _m in _match:
                _n = re.compile(r'\s([0-9]{1,2})')
                p = re.compile(r'@bit([1-7])$').findall(_m)[0]
                nm = [int(x, base=10) for x in _n.findall(_m)]
                funx = getattr(rego_filter, f'f_bitex_{p}')
                temp.append({'f': funx, 'a': nm})
            return temp
        return None

    def parse_v2(self, filgo: str) -> None:
        '''格式化rego文件'''
        __re_dict = {
            'paichu': self.p_paichu,
            'baohan': self.p_baohan,
            'bit': self.p_bit,
            'bitex': self.p_bitex
        }
        if filgo != None:
            self.parse_dict = {}
            index = 1
            for k, pfunc in __re_dict.items():
                env = pfunc(filgo)
                if env != None:
                    for e in env:
                        self.parse_dict.update({index: e})
                        index += 1
            if self.debug:
                print(f'debug {self.parse_dict}')


# class rego filter
class rego_filter:

    @staticmethod
    def f_paichu_r(N: Note, args: List) -> bool:
        '''排除'''
        for _n in N.number:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_paichu_b(N: Note, args: List) -> bool:
        '''排除'''
        for _n in N.tiebie:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_baohan(N: Note, args: List) -> bool:
        '''包含'''
        for _n in N.setnumber_R:
            if _n in args:
                return True
        return False

    @classmethod
    def f_bit_1(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 1)

    @classmethod
    def f_bit_2(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 2)

    @classmethod
    def f_bit_3(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 3)

    @classmethod
    def f_bit_4(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 4)

    @classmethod
    def f_bit_5(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 5)

    @classmethod
    def f_bit_6(cls, N: Note, args: List) -> bool:
        return cls.f_bit(N, args, 6)

    @staticmethod
    def f_bit_7(N: Note, args: List) -> bool:
        for _n in N.tiebie:
            if _n in args:
                return True
        return False

    @staticmethod
    def f_bit(N: Note, args: List, index: int) -> bool:
        '''定位 包含'''
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            if _n not in args:
                return False
        return True

    @classmethod
    def f_bitex_1(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 1)

    @classmethod
    def f_bitex_2(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 2)

    @classmethod
    def f_bitex_3(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 3)

    @classmethod
    def f_bitex_4(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 4)

    @classmethod
    def f_bitex_5(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 5)

    @classmethod
    def f_bitex_6(cls, N: Note, args: List) -> bool:
        return cls.f_bitex(N, args, 6)

    @staticmethod
    def f_bitex_7(N: Note, args: List) -> bool:
        for _n in N.tiebie:
            if _n in args:
                return False
        return True

    @staticmethod
    def f_bitex(N: Note, args: List, index: int) -> bool:
        '''定位 不包含'''
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            if _n in args:
                return False
        return True
