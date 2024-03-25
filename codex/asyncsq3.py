# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-24 22:16:16
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-25 21:58:29
from typing import List, Literal
import aiosqlite, asyncio, random, itertools

DBPATH = 'iosqlite.db'


class AsyncSQLite3:

    def __init__(self, db_path=DBPATH, buffer_size=100):
        self.db_path = db_path
        self.buffer_size = buffer_size
        self.queue = []
        self.db = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        if self.db:
            await self.flush_queue()
            await self.close()

    async def table_exists(self, table_name):
        '''检查数据库中是否存在表'''
        if self.db:
            cursor = await self.db.execute(f"PRAGMA table_info({table_name})")
            return bool(await cursor.fetchone())
        return False

    async def create_ship_table(self):
        '''创建船舰数据表'''
        if self.db:
            await self.db.execute('''
                CREATE TABLE IF NOT EXISTS ship (
                    id INTEGER PRIMARY KEY,
                    R TEXT,
                    B TEXT
                )
            ''')

    async def create_cyns_from_shipid_table(self):
        if self.db:
            await self.db.execute('''
                CREATE TABLE IF NOT EXISTS cyns (
                    id INTEGER PRIMARY KEY,
                    source INTEGER REFERENCES ship(id),
                    target TEXT,
                    count INTEGER
                )
            ''')

    async def check_ship_where_r(self, r:str):
        '''
        存在为 True
        '''
        _temp = False
        if self.db:
            cursor = await self.db.execute(
                "SELECT 1 FROM ship WHERE R = ?", (r,)
            )
            _temp = bool(await cursor.fetchone())
        return _temp

    async def write_ship_row(self, r: str, b: str):
        if self.db:
            await self.write('''INSERT INTO ship (r, b) VALUES (?, ?)''',
                             (r, b))

    async def write_cyns_row(self, sid: int, tid: int, count: int):
        if self.db:
            if sid != tid and count >= 3:
                await self.write(
                    '''
                    INSERT INTO cyns (source, target, count)
                    VALUES (?, ?, ?)
                    ''', (sid, tid, count))

    async def read_ship_rows(self):
        if self.db:
            rows = await self.read('''SELECT * FROM ship''')
        return rows
    
    async def read_cyns_rows(self):
        if self.db:
            rows = await self.read('''SELECT * FROM cyns''')
        return rows

    async def delete_ship(self):
        if self.db:
            await self.db.execute('''
                                DELETE FROM ship
                                ''')
            self.queue.clear()
            await self.db.commit()
            
    async def delete_cyns(self):
        if self.db:
            await self.db.execute('''
                                DELETE FROM cyns
                                ''')
            self.queue.clear()
            await self.db.commit()

    async def connect(self):
        print(f'connection {self.db=}')
        self.db = await aiosqlite.connect(self.db_path)

    async def close(self):
        if self.db:
            await self.db.close()

    async def execute(self, sql, params=None):
        if not self.db:
            await self.connect()

        if params is None:
            params = []

        self.queue.append((sql, params))

        if len(self.queue) >= self.buffer_size:
            await self.flush_queue()

    async def flush_queue(self):
        if self.db:
            while self.queue:
                sql, params = self.queue.pop(0)
                R, _ = params
                print(f'Check {R =}')
                if await self.check_ship_where_r(R) == False:
                    await self.db.execute(sql, params)
                else:
                    print(f'R is in ship {R}')
                    await asyncio.sleep(3)
            await self.db.commit()

    async def read(self, sql, params=None):
        rows = None
        if not self.db:
            await self.connect()

        if params is None:
            params = []
        if self.db:
            cursor = await self.db.execute(sql, params)
            rows = await cursor.fetchall()
        return rows

    async def write(self, sql, params=None):
        try:
            await self.execute(sql, params)
        except Exception as e:
            print(f'{e =}')

# 以下是测试代码
async def main():
    async with AsyncSQLite3() as db:
        # if db.
        if await db.table_exists('ship'):
            await db.delete_ship()
        else:
            await db.create_ship_table()
        
        test = []
        
        for i in range(10):
            _n = []
            _list = [x for x in range(1, 34)]
            for _ in range(6):
                _tx = random.choice(_list)
                if _tx not in _n:
                    _n.append(_tx)
                _list.remove(_tx)
            if i == 3:
                test = _n
            if i==5:
                _n = test

            _t = [random.choice([x for x in range(1, 17)])]
            ns = ' '.join((f'{x:02}' for x in sorted(_n)))
            ts = ' '.join((f'{x:02}' for x in _t))
            # 写入数据
            await db.write_ship_row(ns, ts)
            print(f'{i} {ns =} {ts =}')
    print(f'db is over.')


def parse(row: tuple) -> tuple[int, List[int], List[int]]:
    try:
        id, r, b = row
        id = int(id)
        r = [int(x) for x in r.split(' ')]
        b = [int(x) for x in b.split(' ')]
    except:
        print(f'Unable to parse {row}')
        id = 0
        r = [0]
        b = [0]
    finally:
        return (id, r, b)


async def Compare(z: tuple, comit: AsyncSQLite3):
    s, t = z
    spar = parse(s)
    tpar = parse(t)
    if spar[1] != 0 and tpar[1] != 0:
        jiaoji = (set(spar[1]) & set(tpar[1])).__len__()
        if 6 > jiaoji >= 3:
            await comit.write_cyns_row(spar[0], tpar[0], jiaoji)


async def read():
    async with AsyncSQLite3() as db:
        rows = await db.read_ship_rows()
        
        if rows != None:
            await db.create_cyns_from_shipid_table()
            cyns = itertools.product(rows, rows)
            for zitem in cyns:
                await Compare(zitem, db)


if __name__ == '__main__':
    asyncio.run(main())
