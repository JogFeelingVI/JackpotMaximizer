# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-11 15:05:57

import itertools, re, time
from codex import Tonji


def main():
    print(f'====== {time.time()} ======')
    tjone = Tonji.statistics()
    # Read the list of lists from the file.
    with open('save.log', 'r') as f:
        list_of_lists = [tjone.parse_save(line=line) for line in f]
        for lol in list_of_lists:
            tjone.add(lol)
            
    filter_dict = {k: v for k,v in tjone.same_numbers_dict.items() if len(v)==1}
    grouped = itertools.groupby(filter_dict.items(), lambda x: x[1])
    grouped_ids = [id[0] for id, keys in grouped if len(list(keys))>=6]
    for id in grouped_ids:
        print(f'id {id:>4} lins {tjone.sublists[id].test}')

    # filter_dict = {
    #     k: v
    #     for k, v in filter(whereis, tjone.same_numbers_dict.items())
    # }
    # grouped_dict = itertools.groupby(filter_dict.items(), lambda x: x[1])
    # group_count = 0
    # for key, group in grouped_dict:
    #     # key 是分组的 key，group 是分组元素的迭代器
    #     _t = list(group)
    #     if len(_t) == 6:
    #         print(f'Key: {key}, Values: {_t}')
    #         group_count +=1
    # print(f'group len {group_count}')


if __name__ == "__main__":
    main()
