# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-19 09:58:12
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-28 16:26:26
import sqlite3

db_path = 'my_database.db'

class Sqlite3Database:

    def __init__(self, db_name = db_path):
        self.db_name = db_name
        self.conn = None
        
    def __enter__(self):
        if self.conn == None:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        if self.conn:
            self.conn.close()
        

    def connect(self):
        self.conn = sqlite3.connect(database=self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data (
                    id INTEGER PRIMARY KEY,
                    r_numbers TEXT,
                    b_numbers TEXT
                )
            ''')
            self.conn.commit()

    def add_data(self, r_numbers, b_numbers):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(
                '''
                INSERT INTO data (r_numbers, b_numbers)
                VALUES (?, ?)
            ''', (r_numbers, b_numbers))
            self.conn.commit()
            
    def check_data_r_number_exists(self, r_number):
        """检查 r_number 是否存在于数据库中。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM data WHERE r_numbers = ?", (r_number,))
            return cursor.fetchone() is not None
        else:
            return False

    def read_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM data
            ''')
            return cursor.fetchall()

    def read_data_by_ids(self, ids):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(
                '''
                SELECT * FROM data
                WHERE id IN ({})
            '''.format(','.join(['?'] * len(ids))), ids)
            return cursor.fetchall()
        
    def get_all_data_ids(self):
        """返回数据表中所有 ID 的列表。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM data")
            return [row[0] for row in cursor.fetchall()]
        else:
            return []

    def clear_table_data(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM data
            ''')
            self.conn.commit()

    def is_connected(self):
        """判断数据库连接是否处于活动状态。 这个方法 不在使用"""
        try:
            # 执行一个简单的 SQL 查询来测试连接
            if self.conn is not None:
                return True
            else:
                return False
        except sqlite3.Error:
            return False

    def is_Data_already_exists(self):
        try:
            # 执行一个简单的 SQL 查询来测试连接
            if self.conn is not None:
                cursor = self.conn.cursor()
                cursor.execute("SELECT id FROM data")
                if len(cursor.fetchall()) == 0:
                    return False
                return True
            else:
                return False
        except sqlite3.Error:
            return False
        
    def create_table_cyns(self):
        """创建 cyns 数据表。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cyns (
                    id INTEGER PRIMARY KEY,
                    from_id INTEGER REFERENCES data(id),
                    cyn INTEGER
                )
            ''')
            self.conn.commit()
            
    def add_cyns(self, from_id, cyn):
        """向 cyns 数据表中添加数据。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(
                '''
                INSERT INTO cyns (from_id, cyn)
                VALUES (?, ?)
                ''',
                (from_id, cyn),
            )
            self.conn.commit()
            
    def clear_table_cyns(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM cyns
            ''')
            self.conn.commit()
            
    def drop_table_cyns(self):
        """删除 cyns 数据表。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS cyns")
            self.conn.commit()
            
    def get_smallest_cyns(self, n=100):
        """返回 cyns 数据表中 cyn 最小的前 N 条数据。"""
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(
                '''
                SELECT DISTINCT cyns.from_id, cyns.cyn, data.r_numbers, data.b_numbers
                FROM cyns
                INNER JOIN data ON cyns.from_id = data.id
                GROUP BY cyns.from_id
                ORDER BY cyns.cyn ASC
                LIMIT ?
                ''',
                (n,),
            )
            return cursor.fetchall()
        else:
            return []
