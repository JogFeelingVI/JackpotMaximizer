# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-12 09:03:30

import itertools, re, time
from codex import Tonji

def test():
    tjone = Tonji.statistics()
    tjone.Statistical_length = 4
    # Read the list of lists from the file.
    with open('fps.log', 'r') as f:
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
        print(f'[ {v:>3} ]{tjone.sublists[v].test}')

# def main():
#     print(f'====== {time.time()} ======')
#     tjone = Tonji.statistics()
#     # Read the list of lists from the file.
#     with open('fps.log', 'r') as f:
#         list_of_lists = [tjone.parse_fps(line=line) for line in f]
#         for lol in list_of_lists:
#             tjone.add(lol)
            
#     filter_dict = {k: v for k,v in tjone.same_numbers_dict.items() if len(v)==6}
#     grouped = itertools.groupby(filter_dict.items(), lambda x: x[1])
#     grouped_ids = [id[0] for id, keys in grouped if len(list(keys))>=6]
#     counts = -0 
#     for id in grouped_ids:
#         print(f'id {id:>4} lins {tjone.sublists[id].test}')
#         counts += 1
#         if counts == 5:
#             print('')
#             counts = 0
#     print(f'counts {len(grouped_ids)}')



if __name__ == "__main__":
    test()
