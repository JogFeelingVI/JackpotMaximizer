# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-01-07 14:18:41
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-21 10:07:28

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


def diffMain(result:list=[]):
    diff = diffwhere
    dataForCyn = diff.tasks_futures_proess_mem(result)
    # data i = (996, {4:37,5:1}, [6, 8, 19, 28, 29, 31], [4])
    # data i = (998, {4:46,5:1}, [8, 9, 18, 19, 20, 33], [5])
    # data i = (999, {4:77,5:1}, [3, 4, 10, 25, 29, 33], [5])
    #  (999, {4: 0, 5: 0}, [1, 5, 15, 16, 26, 29], [3])
    # print(f'{dataForCyn=}')
    if dataForCyn.__len__() > 0:
        # dataForCyn = [x for x in dataForCyn if x[1][5] in [2, 3]]
        dataForCyn = sorted(dataForCyn, key= lambda x:x[1][4])
        print(f'min: {dataForCyn[0][1]} max{dataForCyn[-1][1] }')
    else:
        return None
    return dataForCyn


if __name__ == "__main__":
    diffMain()
