# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-03-19 09:58:12
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-03-19 10:12:53
import sqlite3


class Sqlite3Database:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
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
            cursor.execute('''
                SELECT * FROM data
                WHERE id IN ({})
            '''.format(','.join(['?'] * len(ids))), ids)
            return cursor.fetchall()

    def clear_database(self):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM data
            ''')
            self.conn.commit()
