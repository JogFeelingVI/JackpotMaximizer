# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-10-24 19:04:50
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2023-10-27 20:43:30

import re
from typing import List
import pathlib

class Note:

    def __init__(self, n: List[int], T: List[int] | int) -> None:
        """Note

        Args:
            n (List[int]): 1-33 红色号码球
            T (List[int] | int): 1-16 蓝色号码球
        """
        self.number = []
        self.tiebie = []
        for i in sorted(n):
            if 1 <= i <= 33 and n.count(i) == 1:
                self.number.append(i)
        Tx = [T, [T]][isinstance(T, int)]
        for i in sorted(Tx):
            if 1 <= i <= 16 and Tx.count(i) == 1:
                self.tiebie.append(i)
        if self.number.__len__() < 6 or self.tiebie.__len__() == 0:
            raise Exception(f'Note Creation failed {self.number}')

    def filter(self, func) -> None:
        '''
        filter jiekou
        '''
        self.number = list(filter(func, self.number))

    @property
    def setnumber_R(self):
        return set(self.number)

    @property
    def setnumber_B(self):
        return set(self.tiebie)

    def __str__(self) -> str:
        n = ' '.join([f'{num:02d}' for num in self.number])
        t = ' '.join([f'{num:02d}' for num in self.tiebie])
        return f'{n} + {t}'




class rego:
    '''读取rego文件并对列表进行解析'''
    __rego_lines = None
    __parse_dict = []
    __debug = False
    __re_dict = None
    __func = None
    __version = '2023/10/25'

    @property
    def re_dict(self) -> dict:
        if self.__re_dict == None:
            self.__re_dict = {
                'paichu': lambda l:self.__paichu(l),
                'baohan': lambda l:self.__baohan(l),
                'bit': lambda l:self.__bit(l),
                'bitex': lambda l:self.__bitex(l)
            }
        return self.__re_dict

    @property
    def funcx(self) -> dict:
        if self.__func == None:
            self.__func = {
                'paichu': lambda N, a: self.__f_paichu(N, a),
                'baohan': lambda N, a: self.__f_baohan(N, a),
                'bit_1': lambda N, a: self.__f_bit(N, a, 1),
                'bit_2': lambda N, a: self.__f_bit(N, a, 2),
                'bit_3': lambda N, a: self.__f_bit(N, a, 3),
                'bit_4': lambda N, a: self.__f_bit(N, a, 4),
                'bit_5': lambda N, a: self.__f_bit(N, a, 5),
                'bit_6': lambda N, a: self.__f_bit(N, a, 6),
                'bit_7': lambda N, a: self.__f_bit(N, a, 7),
                'bitex_1': lambda N, a: self.__f_bitex(N, a, 1),
                'bitex_2': lambda N, a: self.__f_bitex(N, a, 2),
                'bitex_3': lambda N, a: self.__f_bitex(N, a, 3),
                'bitex_4': lambda N, a: self.__f_bitex(N, a, 4),
                'bitex_5': lambda N, a: self.__f_bitex(N, a, 5),
                'bitex_6': lambda N, a: self.__f_bitex(N, a, 6),
                'bitex_7': lambda N, a: self.__f_bitex(N, a, 7),
            }
        return self.__func

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool) -> bool:
        self.__debug = value
        return self.__debug

    def __init__(self) -> None:
        self.__load_rego()

    def __load_rego(self) -> None:
        '''装载rego文件'''
        rego = pathlib.Path('insx.reg')
        with rego.open(mode='r', encoding='utf-8') as go:
            self.__rego_lines = go.readlines()

    @staticmethod
    def __paichu(line: str) -> dict | None:
        '''排除法检测'''
        _paichu = re.compile(r'^-([ 0-9]+)as [R|B]$')
        if (_match := _paichu.match(line)) != None:
            _n = re.compile('[0-9]{1,2}')
            _p = re.compile('(R|B)$')
            rb = _p.findall(_match.string)
            nm = [int(x, base=10) for x in _n.findall(_match.string)]
            return {'name': 'paichu', 'rb': rb, 'number': nm}
        return None

    @staticmethod
    def __baohan(line: str) -> dict | None:
        _baohan = re.compile(r'^\+([ 0-9]+)$')
        if (_match := _baohan.match(line)) != None:
            _n = re.compile('[0-9]{1,2}')
            nm = [int(x, base=10) for x in _n.findall(_match.string)]
            return {'name': 'baohan', 'rb': ['R'], 'number': nm}
        return None

    @staticmethod
    def __bit(line: str) -> dict | None:
        '''Bit'''
        _bit = re.compile(r'^\+([ 0-9]+)@bit[1-7]$')
        if (_match := _bit.match(line)) != None:
            _n = re.compile(r'\s([0-9]{1,2})')
            p = re.compile(r'@bit([1-7])$').findall(_match.string)[0]
            nm = [int(x, base=10) for x in _n.findall(_match.string)]
            return {'name': f'bit_{p}', 'rb': [], 'number': nm}
        return None

    @staticmethod
    def __bitex(line: str) -> dict | None:
        '''Bit ex'''
        _bit = re.compile(r'^-([ 0-9]+)@bit[1-7]$')
        if (_match := _bit.match(line)) != None:
            _n = re.compile(r'\s([0-9]{1,2})')
            p = re.compile(r'@bit([1-7])$').findall(_match.string)[0]
            nm = [int(x, base=10) for x in _n.findall(_match.string)]
            return {'name': f'bitex_{p}', 'rb': [], 'number': nm}
        return None

    def parse(self) -> None:
        _huanhang = re.compile(r'\\n')
        if self.__rego_lines != None:
            for line in self.__rego_lines:
                line = _huanhang.sub('', line)
                if line.__len__() > 1:
                    for k, kv in self.re_dict.items():
                        enx = kv(line)
                        if enx != None:
                            self.__parse_dict.append(enx)
            if self.debug:
                print(f'debug {self.__parse_dict}')

    @staticmethod
    def __f_paichu(N: Note, args: dict) -> bool:
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

    @staticmethod
    def __f_baohan(N: Note, args: dict) -> bool:
        '''包含'''
        re_args = []
        if args['name'] == 'baohan':
            if 'R' in args['rb']:
                jtwo = N.setnumber_R.intersection(set(args['number']))
                re_args.append([1, 0][jtwo.__len__() > 0])
        return [False, True][1 not in re_args]

    @staticmethod
    def __f_bit(N: Note, args: dict, index: int) -> bool:
        '''定位 包含'''
        re_args = []
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            re_args.append([1, 0][_n in args['number']])
        if index in [7]:
            _n = N.setnumber_B.intersection(set(args['number']))
            re_args.append([1, 0][len(_n) >= 1])
        return [False, True][1 not in re_args]

    @staticmethod
    def __f_bitex(N: Note, args: dict, index: int) -> bool:
        '''定位 不包含'''
        re_args = []
        if index in [1, 2, 3, 4, 5, 6]:
            _n = N.number[index - 1]
            re_args.append([1, 0][_n not in args['number']])
        if index in [7]:
            _n = N.setnumber_B.intersection(set(args['number']))
            re_args.append([1, 0][len(_n) == 0])

        return [False, True][1 not in re_args]

    def filtration(self, N: Note) -> bool:
        if self.__parse_dict != None:
            for linex in self.__parse_dict:
                if linex != None and isinstance(linex, dict):
                    funx = self.funcx[linex['name']]
                    refv = funx(N, linex)
                    if self.debug:
                        print(
                            f'filtration {linex["name"]} -> {refv} args {linex}'
                        )
                    if refv is False:
                        return refv
            return True
        return True