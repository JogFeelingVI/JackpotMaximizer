# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-04-02 22:30:53

import functools
import itertools, re, time
from codex import sq3database, tonji, diffwhere

# def test():

#     with sq3database.Sqlite3Database('my_database.db') as sq3:

#         if sq3.is_connected() == False:
#             print(f'Sqlite3Database connection failed.')
#             return
#         sq3data = sq3.read_data()
#         if sq3data == None or len(sq3data) == 0:
#             print(f'Sqlite3Database database is empty.')
#             return
#         tjone = tonji.statistics()
#         tjone.Statistical_length = 4
#         # Read the list of lists from the file.
#         for sq3_item in sq3data:
#             N = tonji.parseSublist(sq3_item)
#             tjone.add(N)

#         print(f'====== {time.time()} ======')
#         vid = []
#         for k, v in  tjone.same_numbers_dict.items():
#             print(f'key {k} len {len(v)} value {v[-3::]}...')
#             if len(v) == 4:
#                 [vid.append(x) for x in v if x not in vid]
#         print(f'====== lens {tjone.same_numbers_dict.keys().__len__()}/{vid.__len__()} ======')
#         filter_data = sq3.read_data_by_ids(vid)
#         if filter_data != None:
#             for fItem in filter_data:
#                 id, r, b = fItem
#                 print(f'id: {id:>3} / {r} + {b}')
#         else:
#             print('No data matching the filter criteria.')


def diffMain(show:bool = True, result:list=[]) -> tuple[int,int, list, list]:
    diff = diffwhere
    dataForCyn = diff.tasks_futures_proess_mem(result)
    # data i = (996, 48, [6, 8, 19, 28, 29, 31], [4])
    # data i = (998, 46, [8, 9, 18, 19, 20, 33], [5])
    # data i = (999, 77, [3, 4, 10, 25, 29, 33], [5])
    dataForCyn = sorted(dataForCyn, key= lambda x:x[1])
    fromids = dataForCyn[0]
        
    
    if show:
        for df in dataForCyn:
            fromid, cyn, n, t = df
        # Nr_str = ' '.join([f"{x:02}" for x in _s.rNumber])
        # Nb_str = ' '.join([f"{x:02}" for x in _s.bNumber])
            print(f'id {fromid:>4} / cyn {cyn} * {n} + {t}')
    return fromids


if __name__ == "__main__":
    diffMain()
