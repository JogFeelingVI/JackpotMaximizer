# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-10 20:02:11
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-09 16:57:14
import itertools, re, operator, dataclasses
from typing import Any, List, Generator
from codex import glns_v2, note


@dataclasses.dataclass
class sublist:
    resute: list
    test: str


class statistics:
    """
    Finds all the sublists in a list that have the same numbers.

    Args:
        list_of_lists: A list of lists, where each sublist contains a set of numbers.
        num_of_same_numbers: The number of numbers that must be the same in each sublist.

    Returns:
        A list of all the sublists that have the same numbers.
    """
    same_numbers_dict = {}
    num_of_same_numbers = 5
    sublists = []

    @property
    def nosn(self):
        return self.num_of_same_numbers

    @nosn.setter
    def nosn(self, Var: int):
        if 2 <= Var <= 5:
            self.num_of_same_numbers = Var

    def parse_save(self, line) -> sublist:
        recs = [(re.compile(r'^(date|args).*'), lambda x: None),
                (re.compile(r'^\[-\]\s[ 0-9]+'),
                 lambda x: [int(gz) for gz in x])]
        result = []
        for r, handle in recs:
            match = r.match(line)
            if match:
                result = handle(match.group(0).split()[1::])
                break
        return sublist(result, line.replace('\n', ''))

    def parse_fps(self, line) -> sublist:
        recs = [(re.compile(r'^(date|args).*'), lambda x: None),
                (re.compile(r'N:([0-9]+(?: [0-9]+)*)'),
                 lambda x: [int(gz) for gz in x])]
        result = []
        for r, handle in recs:
            match = r.search(line)
            if match:
                result = handle(match.group(1).split())
                break
        return sublist(result, line.replace('\n', ''))

    def __init__(self):
        self.same_numbers_dict = {}
        self.sublists = []

    def add(self, N: sublist):
        ''''''
        if N.resute == None and N not in self.sublists:
            # 确保数据不会重复
            return
        self.sublists.append(N)
        n_index = self.sublists.index(N)
        combinations_sublist = itertools.combinations(N.resute, self.nosn)
        for com_sublist in combinations_sublist:
            sort_com_sublist = sorted(com_sublist)
            tuple_sublist = tuple(sort_com_sublist)
            # Add the tuple sublist to the dictionary, along with the original sublist.
            if tuple_sublist not in self.same_numbers_dict:
                self.same_numbers_dict[tuple_sublist] = [n_index]
            else:
                if n_index not in self.same_numbers_dict[tuple_sublist]:
                    self.same_numbers_dict[tuple_sublist].append(n_index)

    def where_key(self) -> None:
        '''where is key'''
        pass
    
    @staticmethod
    def fmt_key(key):
            return ''.join((f'{x:>02}' for x in key))

    def echo(self, lines = None):
        f = lambda x: len(x[1])
        for key, subs in sorted(self.same_numbers_dict.items(), key=f, reverse=True):
            flg = False
            match lines:
                case list()|tuple():
                    if any(item in subs for item in lines):
                        flg = True
                case int():
                    if lines in subs:
                        flg = True
                case _:
                    flg = False
            if flg:
                print(f'statistics {self.fmt_key(key)}, lens {subs.__len__()}, * {subs}')
            else:
                print(f'statistics {self.fmt_key(key)}, lens {subs.__len__()}, {subs}')
        
