# -*- coding: utf-8 -*-
"""
This module is started by proxy.py to prepare all environment.
"""
import os
import json
import sqlite3
from log import Log

class Setup:
    """
    @brief      Class for setup environment, create necessary folder and files.
    """

    def __init__(self):
        create_dir('log',"log directory created")

        create_config(12000,'config.json',"config file created with default values")

        create_cache_db('cache.sqlite',"cache DB created")

    @property
    def config(self):

        """
        @brief      property to get json config file in a dictionary.
        
        @param      self  The object
        
        @return     void method.
        """

        with open('config.json') as cfg_file:
            return json.load(cfg_file)


def create_cache_db(_db_file, _log_msg):
    cache_db= os.path.join(os.getcwd(), _db_file)
    if not os.path.exists(cache_db):
        conn = sqlite3.connect(_db_file)
        c = conn.cursor()
        sql = '''create table if not exists CACHE(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    DATA BLOB,
                    REQUISITION TEXT,
                    VALIDITY TIMESTAMP);'''
        c.execute(sql)
        conn.close()
        Log(_log_msg)

def create_dir(_dir_name, _log_msg):
    dir = os.path.join(os.getcwd(), _dir_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
        Log(_log_msg)

def create_config(_port, _file, _log_msg):
    config = os.path.join(os.getcwd(), _file)
    if not os.path.exists(config):
        jsonfile = open(_file, 'w')
        json.dump({'port': str(_port)}, jsonfile)
        jsonfile.flush()
        jsonfile.close()
        Log(_log_msg)