# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-10-24 19:04:50
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-25 20:25:27

import re, time
from typing import List
import pathlib
try:
    from codex.glns_v2 import Note
    filenam = 'insx.reg'
except:
    from Codex.glns_v2 import Note
    filenam = 'rego'


class rego:
    '''读取rego文件并对列表进行解析'''
    rego_lines = None
    __debug = False

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool) -> bool:
        self.__debug = value
        return self.__debug

    def __init__(self) -> None:
        self.load_rego_v2()
        self.parse_v2()
        self.Func = {
            'paichu_r': self.f_paichu_r,
            'paichu_b': self.f_paichu_b,
            'baohan': self.f_baohan,
            'bit_1': self.f_bit_1,
            'bit_2': self.f_bit_2,
            'bit_3': self.f_bit_3,
            'bit_4': self.f_bit_4,
            'bit_5': self.f_bit_5,
            'bit_6': self.f_bit_6,
            'bit_7': self.f_bit_7,
            'bitex_1': self.f_bitex_1,
            'bitex_2': self.f_bitex_2,
            'bitex_3': self.f_bitex_3,
            'bitex_4': self.f_bitex_4,
            'bitex_5': self.f_bitex_5,
            'bitex_6': self.f_bitex_6,
            'bitex_7': self.f_bitex_7,
        }

    def load_rego_v2(self) -> None:
        '''装载rego文件'''
        rego = pathlib.Path(filenam)
        with rego.open(mode='r', encoding='utf-8') as go:
            self.rego_lines = go.read()

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
                    temp.append({'name': 'paichu_r', 'rb': '', 'number': nm})
                if 'B' in rb:
                    temp.append({'name': 'paichu_b', 'rb': '', 'number': nm})
            return temp
        return None

    def p_baohan(self, line: str) -> List | None:
        _baohan = re.compile(r'^\+[ 0-9]+as R$', flags=re.M)
        temp = []
        if (_match := _baohan.findall(line)) != None:
            for _m in _match:
                _n = re.compile('[0-9]{1,2}')
                nm = [int(x, base=10) for x in _n.findall(_m)]
                temp.append({'name': 'baohan', 'rb': '', 'number': nm})
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
                temp.append({'name': f'bit_{p}', 'rb': '', 'number': nm})
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
                temp.append({'name': f'bitex_{p}', 'rb': '', 'number': nm})
            return temp
        return None

    def parse_v2(self) -> None:
        '''格式化rego文件'''
        __re_dict = {
            'paichu': self.p_paichu,
            'baohan': self.p_baohan,
            'bit': self.p_bit,
            'bitex': self.p_bitex
        }
        if self.rego_lines != None:
            self.parse_dict = {}
            index = 1
            for k, pfunc in __re_dict.items():
                env = pfunc(self.rego_lines)
                if env != None:
                    for e in env:
                        self.parse_dict.update({index: e})
                        index += 1
            if self.debug:
                print(f'debug {self.parse_dict}')

    def f_paichu_r(self, N: Note, args: dict) -> bool:
        '''排除'''
        Asnum = args['number']
        for _n in N.number:
            if _n in Asnum:
                return False
        return True

    def f_paichu_b(self, N: Note, args: dict) -> bool:
        '''排除'''
        Asnum = args['number']
        for _n in N.tiebie:
            if _n in Asnum:
                return False
        return True

    def f_baohan(self, N: Note, args: dict) -> bool:
        '''包含'''
        Asnum = args['number']
        for _n in N.setnumber_R:
            if _n in Asnum:
                return True
        return False
    
    def f_bit_1(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 1)
    
    def f_bit_2(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 2)
    
    def f_bit_3(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 3)
    
    def f_bit_4(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 4)
    
    def f_bit_5(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 5)
    
    def f_bit_6(self, N: Note, args: dict) -> bool:
        return self.f_bit(N, args, 6)
    
    def f_bit_7(self, N: Note, args: dict) -> bool:
        Asnum = args['number']
        for _n in N.tiebie:
            if _n in Asnum:
                return True
        return False

    def f_bit(self, N: Note, args: dict, index: int) -> bool:
        '''定位 包含'''
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            if _n not in args['number']:
                return False
        return True
    
    def f_bitex_1(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 1)
    
    def f_bitex_2(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 2)
    
    def f_bitex_3(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 3)
    
    def f_bitex_4(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 4)
    
    def f_bitex_5(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 5)
    
    def f_bitex_6(self, N: Note, args: dict) -> bool:
        return self.f_bitex(N, args, 6)
    
    def f_bitex_7(self, N: Note, args: dict) -> bool:
        Asnum = args['number']
        for _n in N.setnumber_B:
            if _n in Asnum:
                return False
        return True

    def f_bitex(self, N: Note, args: dict, index: int) -> bool:
        '''定位 不包含'''
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            if _n in args['number']:
                return False
        return True

    def filtration_olde(self, N: Note) -> bool:
        '''
        这个程序急需优化
        {'name': 'paichu', 'rb': ['R'], 'number': [33, 27], 'func': <function rego.p_paichu.<locals>.<lambda> at 0x10b7c49a0>}
        '''
        if self.parse_dict.keys() != []:
            for _, linex in self.parse_dict.items():
                funx = self.Func[linex['name']]
                refv = funx(N, linex)
                if self.debug:
                    print(f'filtration {linex["name"]} -> {refv} args {linex}')
                if refv is False:
                    return refv
            return True
        else:
            print(f'[R] this parse dict is None')
        return True

    def filtration(self, N: Note) -> bool:
        '''优化后的程序'''
        NLs = [N] * self.parse_dict.keys().__len__()
        rext = map(self.anis, NLs, self.parse_dict.values())
        if False in rext:
            return False
        return True

    def anis(self, N: Note, linex: dict) -> bool:
        '''{name: paichu, rb: [R], number: [10, 30, 15, 11]}'''
        funx = self.Func[linex['name']](N, linex)
        return funx
