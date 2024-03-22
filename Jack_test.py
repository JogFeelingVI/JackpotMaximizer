# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-22 13:50:54
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-22 15:16:43
import asyncio, concurrent.futures, random, time


def task(index: int):
    if index < 3:
        index = 3
    en = [index / x for x in range(2, random.randint(100, 1000))]
    return sum(en) / en.__len__()


async def Gonren(name='', id=1, max=1000):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(task, i) for i in range(1, max)]
        completed = 0
        futures_len = futures.__len__()
        iStorage = []
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            print(
                f'\033[K[P] completed {name:>5} {completed/futures_len*100:.4f}% tasks completed.',
                end='\r')
            iStorage.append(future.result())
        print(f'\033[K[{name:>5}] ID = {id} completed 100%.')
    return iStorage


async def main():
    base = 'arssdDzXdiusnHG2opLJu7Bnx5fTy9'
    lisrt = []
    for x in range(10):
        name = random.choices(base, k=5)
        maxs = random.randint(1000, 10000)
        lisrt.append(Gonren(''.join(name), x,  maxs))

    print(f'{time.strftime("%X"):_^20}')
    await asyncio.sleep(3)
    rest = asyncio.gather(*lisrt)
    print(f'Test done! "{time.strftime("%X")}"')


if __name__ == "__main__":
    asyncio.run(main())
