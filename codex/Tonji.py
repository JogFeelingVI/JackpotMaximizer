# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-10 20:02:11
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-19 21:20:32
import itertools, re, operator, dataclasses
from typing import Any, List, Generator


@dataclasses.dataclass
class sublist:
    id: int
    rNumber: list
    bNumber: list
    
    
def parseSublist(item = (1, '01 02 11 15 23 32', '13')):
    id, r, b = item
    r = [int(x) for x in r.split(' ')]
    b = [int(x) for x in b.split(' ')]
    return sublist(id, r, b)


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
    
    sublists = []
    __Statistical_length = 5

    @property
    def Statistical_length(self):
        return self.__Statistical_length

    @Statistical_length.setter
    def Statistical_length(self, Var: int):
        if 2 <= Var <= 6:
            self.__Statistical_length = Var


    def __init__(self):
        self.same_numbers_dict = {}

    def add(self, N: sublist):
        ''''''
        if N.rNumber == [] or N.bNumber == '' or N.rNumber == [] or N.id in self.sublists:
            # 确保数据不会重复
            return
        # print(f'debug {N} / {N.resute[0:self.Statistical_length]}')
        combinations_sublist = tuple(N.rNumber[0:self.Statistical_length])
        # Add the tuple sublist to the dictionary, along with the original sublist.
        if combinations_sublist not in self.same_numbers_dict:
            self.same_numbers_dict[combinations_sublist] = [N.id]
        else:
            if N.id not in self.same_numbers_dict[combinations_sublist]:
                self.same_numbers_dict[combinations_sublist].append(N.id)
    
    
    # def where_is(self, key=None, value=None, operator="=="):
    #     '''where is key'''
    #     # Check if the operator is valid
    #     valid_operators = ["==", "!=", "+", "-"]
    #     if operator not in valid_operators:
    #         raise ValueError("Invalid operator: {}".format(operator))
    #     # key
    #     match key:
    #         case None:
    #             key=lambda x:x[1]
    #         case 'key'| 'k'| 0 |'0':
    #             key = lambda x:x[0]
    #         case 'value' | 'v' | 1 |'1':
    #             key = lambda x:x[1]
    #         case _:
    #             key = key
    #     # value        
    #     match value:
    #         case None:
    #             value = {}
    #         case int():
    #             value = set([value])
    #         case str():
    #             value = set([int(value)])
    #     # Define the filter function based on the operator
    #     match operator:
    #         case "==":
    #             filter_func = lambda x:self.fix_val(key(x=x)) == value
    #         case "!=":
    #             filter_func = lambda x:self.fix_val(key(x=x)) != value
    #         case "+":
    #             filter_func = lambda x:self.fix_val(key(x=x)) & set(value)
    #         case "-":
    #             filter_func = lambda x:self.fix_val(key(x=x)) - set(value)
    #         case _:
    #             filter_func = lambda x: key(x=x) == key(x=x)
        # Filter the dictionary using the filter function
        #filtered_keys = filter(filter_func, self.same_numbers_dict.items())
        # Convert the filtered keys to a list and return it
        # return filter_func

    # @staticmethod
    # def fix_val(val):
    #     match val:
    #         case int():
    #             return set([val])
    #         case list()|tuple():
    #             return set(val)
    #         case _:
    #             return set([val])
    
    # @staticmethod
    # def fmt_key(key):
    #         return ''.join((f'{x:>02}' for x in key))

    # def echo(self,dic=None, lines = None):
    #     match dic:
    #         case None:
    #             dic = self.same_numbers_dict
    #         case dict():
    #             pass
    #         case _:
    #             raise ValueError('dic type only DICT')
    #     f = lambda x: len(x[1])
    #     for key, subs in sorted(dic.items(), key=f, reverse=True):
    #         flg = False
    #         match lines:
    #             case list()|tuple():
    #                 if any(item in subs for item in lines):
    #                     flg = True
    #             case int():
    #                 if lines in subs:
    #                     flg = True
    #             case _:
    #                 flg = False
    #         if flg:
    #             print(f'statistics {self.fmt_key(key)}, lens {subs.__len__()}, * {subs}')
    #         else:
    #             print(f'statistics {self.fmt_key(key)}, lens {subs.__len__()}, {subs}')
        
