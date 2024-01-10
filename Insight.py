# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-10 16:57:33

import itertools, re, time
from codex import Tonji


def main():
    print(f'====== {time.time()} ======')
    tjone = Tonji.statistics()
    # Read the list of lists from the file.
    with open('fps.log', 'r') as f:
        list_of_lists = [tjone.parse_fps(line=line) for line in f]
        for lol in list_of_lists:
            tjone.add(lol)
    whereis = tjone.where_is(key=lambda x: len(x[1]), value=1, operator='==')

    filter_dict = {
        k: v
        for k, v in filter(whereis, tjone.same_numbers_dict.items())
    }
    grouped_dict = itertools.groupby(filter_dict.items(), lambda x: x[1])
    for key, group in grouped_dict:
        # key 是分组的 key，group 是分组元素的迭代器
        _t = list(group)
        if len(_t) == 6:
            print(f'Key: {key}, Values: {_t}')


if __name__ == "__main__":
    main()
