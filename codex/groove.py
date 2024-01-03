# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-20 09:02:19
# @Last Modified by:   Your name
# @Last Modified time: 2024-01-03 22:19:22
import heapq, random, json, pathlib
from typing import Any, List
from codex import ospath

RC = [f'bit_{x}' for x in range(1, 7)]
BC = ['bit_7']


def bitx_read() -> dict | None:
    bitx = ospath.findAbsp.file_path('bitx.json')
    bitp = pathlib.Path(bitx)
    if bitp.exists():
        with bitp.open(mode='r', encoding='utf-8') as bit:
            return json.loads(bit.read())
    return


class random_ex:

    def __init__(self,
                 json_data: dict,
                 max_length: int,
                 RBC: List = RC) -> None:
        '''
        json_data bitx_read return
        L lenth max 19 min 6
        rc = groove.RC or groove.BC
        '''
        try:
            # Validate and process json_data
            self._init_complete = False
            if not isinstance(json_data, dict):
                raise ValueError("json_data must be a dictionary")

            if 'bit_7' in RBC:
                if 1 <= max_length >= 8:
                    raise ValueError(
                        "max_length value exceeds the limit, bit_7 is 1~8")

            if 'bit_7' not in RBC:
                if 6 <= max_length >= 19:
                    raise ValueError(
                        "max_length value exceeds the limit, bit_1~6 is 6~19")

            self.max_length = max_length
            self.bitx = {k: v for k, v in json_data.items() if k in RBC}
            self._init_complete = True
        except ValueError as e:
            print(e)
            
    def whereiskey(self, key:str) -> list[int]|None:
        '''
        根据key来随机数字
        '''
        try:
            value = self.bitx.get(key, list(self.bitx.values())[0])
            np = [int(x) for x in value.keys()]
            wp = [value[f'{x}'] for x in np]
            return random.choices(np, weights=wp, k=3)
        except:
            return None
        

    def randbitx(self, sink: int):
        '''
        from bitx random 
        这里有很大的问题
        #? 1, 2, 3, 4, 5, 6, 7, 8
        '''
        keyd = f'bit_{sink+1}'
        match keyd:
            case 'bit_7'|'bit_1'|'bit_2'|'bit_3'|'bit_4'|'bit_5'|'bit_6':
                return self.whereiskey(key=keyd)
            case _:
                keyr = f'bit_{random.randint(1, 7)}'
                return self.whereiskey(key=keyr)

    def creation(self):
        """
        Creates a random array of integers with a maximum length using heapq.
        Args:
            max_length: The maximum length of the array.
        Returns:
            A random array of integers with a maximum length.
        """

        # Create a heap of unique random numbers
        random_heap = []
        while len(random_heap) < self.max_length:
            rdb = self.randbitx(len(random_heap))
            if rdb != None:
                for n in rdb:
                    if n not in random_heap:
                        heapq.heappush(random_heap, n)
                        break

        # Create a list of random numbers from the heap
        random_array = []
        while random_heap:
            random_number = heapq.heappop(random_heap)
            random_array.append(random_number)

        # Return the random array
        return random_array

    def get_number_v2(self):
        return self.creation()


def main():
    print(f"Hello, World! {RC}")
    ex = bitx_read()
    if ex != None:
        r = random_ex(ex, 18, RC)
        print(f'debug {r.get_number_v2()}')


if __name__ == "__main__":
    main()
