# -*- coding: utf-8 -*-
"""
This module is started by proxy.py to prepare all environment.
"""
import os
import json
import sqlite3
from log import Log

__docformat__ = 'reStructuredText'


class Setup:
    """
    When this class is instanced it verify if all environment is ready to run ProxY, if isn't this creates de
    necessary files:
    
        * Log directory
        * Config file
        * Cache DB
    """

    def __init__(self):
        create_dir('log', "log directory created")
        create_config(12000, 'config.json', "config file created with default values")
        create_cache_db('cache.sqlite', "cache DB created")

    @property
    def config(self):
        """
        property to get json config file in a dictionary
        
        :return: config dictionary
        """
        with open('config.json') as cfg_file:
            return json.load(cfg_file)


def create_cache_db(_db_file, _log_msg):
    """
    Creates a sqlite3 db if not exists and create CACHE table inside this

    :param _db_file: the db file name
    :param _log_msg: message log for DB creation 
    """
    cache_db = os.path.join(os.getcwd(), _db_file)
    if not os.path.exists(cache_db):
        conn = sqlite3.connect(_db_file)
        c = conn.cursor()
        sql = '''create table if not exists CACHE(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    REQUEST_METHOD TEXT,
                    REQUEST_PATH TEXT,
                    REQUEST_PROTOCOL TEXT,
                    REQUEST_HEADERS TEXT,
                    REQUEST_BODY BLOB,
                    RESPONSE_STATUS_CODE TEXT,
                    RESPONSE_STATUS_MESSAGE TEXT,
                    RESPONSE_PROTOCOL TEXT,
                    RESPONSE_HEADERS TEXT,
                    RESPONSE_BODY BLOB,
                    CACHE_VALIDITY TEXT);'''
        c.execute(sql)
        conn.close()
        Log(_log_msg)


def create_dir(_dir_name, _log_msg):
    """
    This method verify if a given directory (**_dir_name**) exists and if isn't creates.
    
    :param _dir_name: directory name 
    :param _log_msg: log message for directory creation
    """
    dir = os.path.join(os.getcwd(), _dir_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
        Log(_log_msg)


def create_config(_port, _file, _log_msg):
    """
    Create the config.json file if this don't exists.
    
    :param _port: the port value for server
    :param _file: config file name
    :param _log_msg: log message for the config creation
    """
    config = os.path.join(os.getcwd(), _file)
    if not os.path.exists(config):
        jsonfile = open(_file, 'w')
        json.dump({'port': str(_port),
                   'auto_increment_port': 'True',
                   'cache': 'False'}, jsonfile)
        jsonfile.flush()
        jsonfile.close()
        Log(_log_msg)
