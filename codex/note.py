# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2023-12-27 09:03:21
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-02 15:29:46

import heapq


class Note:
    __set_r = None
    __set_b = None

    def __init__(self, n: list[int], T: list[int] | int) -> None:
        """Note
        Args:
            n (List[int]): 1-33 红色号码球
            T (List[int] | int): 1-16 蓝色号码球
        """
        _T = [T, [T]][isinstance(T, int)]
        if len(set(n)) >= 6 and max(n) <= 33 and min(n) >= 1:
            self.number = list(heapq.merge(n, []))
        else:
            raise ValueError(f'red balls must contain at least 6 integers {n}')
        if 16>= len(_T) >= 1 and max(_T) <= 16 and min(_T) >= 1:
            self.tiebie = list(heapq.merge(_T, []))
        else:
            raise ValueError(f'The blue ball must have at least one {_T}')

    def index(self, i: int) -> int:
        return self.number[i - 1]

    @property
    def setnumber_R(self):
        if self.__set_r == None:
            self.__set_r = frozenset(self.number)
        return self.__set_r

    @property
    def setnumber_B(self):
        if self.__set_b == None:
            self.__set_b = frozenset(self.tiebie)
        return self.__set_b

    def __str__(self) -> str:
        n = ' '.join([f'{num:02d}' for num in self.number])
        t = ' '.join([f'{num:02d}' for num in self.tiebie])
        return f'{n} + {t}'
