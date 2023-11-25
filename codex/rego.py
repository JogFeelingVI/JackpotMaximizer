# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-10-24 19:04:50
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-11-25 17:58:21

import re, time
from typing import List
import pathlib
from codex.glns_v2 import Note


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
            'paichu': lambda N, a: self.f_paichu(N, a),
            'baohan': lambda N, a: self.f_baohan(N, a),
            'bit_1': lambda N, a: self.f_bit(N, a, 1),
            'bit_2': lambda N, a: self.f_bit(N, a, 2),
            'bit_3': lambda N, a: self.f_bit(N, a, 3),
            'bit_4': lambda N, a: self.f_bit(N, a, 4),
            'bit_5': lambda N, a: self.f_bit(N, a, 5),
            'bit_6': lambda N, a: self.f_bit(N, a, 6),
            'bit_7': lambda N, a: self.f_bit(N, a, 7),
            'bitex_1': lambda N, a: self.f_bitex(N, a, 1),
            'bitex_2': lambda N, a: self.f_bitex(N, a, 2),
            'bitex_3': lambda N, a: self.f_bitex(N, a, 3),
            'bitex_4': lambda N, a: self.f_bitex(N, a, 4),
            'bitex_5': lambda N, a: self.f_bitex(N, a, 5),
            'bitex_6': lambda N, a: self.f_bitex(N, a, 6),
            'bitex_7': lambda N, a: self.f_bitex(N, a, 7),
        }

    def load_rego_v2(self) -> None:
        '''装载rego文件'''
        rego = pathlib.Path('insx.reg')
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
                temp.append({
                    'name': 'paichu',
                    'rb': rb,
                    'number': nm
                })
            return temp
        return None

    def p_baohan(self, line: str) -> List | None:
        _baohan = re.compile(r'^\+[ 0-9]+as R$', flags=re.M)
        temp = []
        if (_match := _baohan.findall(line)) != None:
            for _m in _match:
                _n = re.compile('[0-9]{1,2}')
                nm = [int(x, base=10) for x in _n.findall(_m)]
                temp.append({
                    'name': 'baohan',
                    'rb': '',
                    'number': nm
                })
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
                temp.append({
                    'name': f'bit_{p}',
                    'rb': '',
                    'number': nm
                })
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
                temp.append({
                    'name': f'bitex_{p}',
                    'rb': '',
                    'number': nm})
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

    def f_paichu(self, N: Note, args: dict) -> bool:
        '''排除'''
        re_args = []
        if args['name'] == 'paichu':
            if 'R' in args['rb']:
                jtwo = N.setnumber_R.intersection(set(args['number']))
                re_args.append([1, 0][jtwo.__len__() == 0])
            if 'B' in args['rb']:
                jtwo = N.setnumber_B.intersection(set(args['number']))
                re_args.append([1, 0][jtwo.__len__() == 0])
        return [False, True][1 not in re_args]

    def f_baohan(self, N: Note, args: dict) -> bool:
        '''包含'''
        re_args = []
        if args['name'] == 'baohan':
            jtwo = N.setnumber_R.intersection(set(args['number']))
            re_args.append([1, 0][jtwo.__len__() > 0])
        return [False, True][1 not in re_args]

    def f_bit(self, N: Note, args: dict, index: int) -> bool:
        '''定位 包含'''
        re_args = []
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            re_args.append([1, 0][_n in args['number']])
        if index in [7]:
            _n = N.setnumber_B.intersection(set(args['number']))
            re_args.append([1, 0][len(_n) >= 1])
        return [False, True][1 not in re_args]

    def f_bitex(self, N: Note, args: dict, index: int) -> bool:
        '''定位 不包含'''
        re_args = []
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            re_args.append([1, 0][_n not in args['number']])
        if index in [7]:
            _n = N.setnumber_B.intersection(set(args['number']))
            re_args.append([1, 0][len(_n) == 0])
        return [False, True][1 not in re_args]

    def filtration_olde(self, N: Note) -> bool:
        '''
        这个程序急需优化
        {'name': 'paichu', 'rb': ['R'], 'number': [33, 27], 'func': <function rego.p_paichu.<locals>.<lambda> at 0x10b7c49a0>}
        '''
        if self.parse_dict.keys() != []:
            for i, linex in self.parse_dict.items():
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
        NLs = [N] * self.parse_dict.__len__()
        rext = map(self.anis, NLs, self.parse_dict)
        if False in rext:
            return False
        return True

    def anis(self, N: Note, linex: dict) -> bool:
        '''{name: paichu, rb: [R], number: [10, 30, 15, 11]}'''
        funx = linex['func'](N, linex)
        return funx
