# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-19 15:00:20

import itertools, re, time
from codex import Tonji

def test():
    tjone = Tonji.statistics()
    tjone.Statistical_length = 6
    # Read the list of lists from the file.
    with open('save.log', 'r') as f:
        list_of_lists = [tjone.parseSublist(line=line) for line in f]
        for lol in list_of_lists:
            tjone.add(lol)
            
    # for lens in range()
    filter_dict = {k: v for k,v in tjone.same_numbers_dict.items()}
    print(f'====== {time.time()} ======')
    vid = []
    for k, v in filter_dict.items():
        print(f'key {k} len {len(v)} value {v}')
        if len(v) == 1:
            [vid.append(x) for x in v if x not in vid]
    print(f'====== lens {filter_dict.keys().__len__()}/{vid.__len__()} ======')
    for v in vid:
        print(f'{tjone.sublists[v].test}')




if __name__ == "__main__":
    test()
