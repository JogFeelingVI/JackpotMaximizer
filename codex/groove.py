# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2023-12-20 09:02:19
# @Last Modified by:   Your name
# @Last Modified time: 2023-12-22 09:13:13
import heapq, random, json, pathlib
from typing import Any, List

RC = [f'bit_{x}' for x in range(1, 7)]
BC = ['bit_7']


def bitx_read() -> dict | None:
    bitx = pathlib.Path('bitx.json')
    if bitx.exists():
        with bitx.open(mode='r', encoding='utf-8') as bit:
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

            if 'bit_4' in RBC:
                if 6 <= max_length >= 19:
                    raise ValueError(
                        "max_length value exceeds the limit, bit_1~6 is 6~19")

            self.max_length = max_length
            self.bitx = {k: v for k, v in json_data.items() if k in RBC}
            self._init_complete = True
        except ValueError as e:
            print(e)

    def randbitx(self, sink: int):
        '''from bitx random'''
        if self.max_length == 6:
            name = f'bit_{sink + 1}'
            key = self.bitx.get(name, {})
            np = [int(x) for x in key.keys()]
            wp = [key[f'{x}'] for x in np]
            random_number = random.choices(np, weights=wp, k=3)
            return random_number
        if self.max_length > 6:
            if 'bitxe' not in vars(self):
                self.bitxe = {}
                for item in self.bitx.values():
                    for k, v in item.items():
                        kv = self.bitxe.get(int(k), 0) + v
                        self.bitxe.update({int(k): kv})

            np = [x for x in self.bitxe.keys()]
            wp = [self.bitxe[x] for x in np]
            random_number = random.choices(np, weights=wp, k=3)
            return random_number
        return [
            random.randint(1, 33),
            random.randint(1, 33),
        ]

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
            for n in self.randbitx(len(random_heap)):
                # random_number = random.randint(1, 33)
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
        r = random_ex(ex, 7, BC)
        print(f'debug {r.creation()}')


if __name__ == "__main__":
    main()
