import os
import sqlite3
from log import Log
from time import gmtime, strftime


class Cache:
    def __init__(self):
        self.conn = sqlite3.connect('cache.sqlite')
        self.cursor = self.conn.cursor()

    def insert_data(self, _data, _requisition, _validity):
        sql = "INSERT INTO CACHE (DATA, REQUISITION, VALIDITY) VALUES (?, ?, ?);"
        self.cursor.execute(sql, [sqlite3.Binary(_data), _requisition, _validity])
        self.conn.commit()
        Log("Data stored in cache DB")
