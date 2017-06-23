import os
import sqlite3
import json
from log import Log
from parser import Parser
from time import gmtime, strftime, time


class Cache:
    def __init__(self):
        self.conn = sqlite3.connect('cache.sqlite')
        self.cursor = self.conn.cursor()

    def store_cache(self, _request, _response):
        try:
            headers_request, body_request = Parser().http_to_dict(_request)
            headers_response, body_response = Parser().http_to_dict(_response)

            if headers_response['protocol'] != 'HTTP/1.1':
                return

            if 'Cache-Control' not in headers_response:
                return

            if ('no-cache' or 'no-store' or 'private') in headers_response['Cache-Control']:
                return

            cache_validity = time()
            if ('max-age' or 's-maxage') in headers_response['Cache-Control']:

                cache_list= headers_response['Cache-Control'].replace('=', ',').split(',')
                cache_list = [i.strip() for i in cache_list]

                if cache_list.index('max-age') != -1:
                    age_index=cache_list.index('max-age')
                elif cache_list.index('s-maxage') != -1:
                    age_index = cache_list.index('s-maxage')
                else:
                    age_index=-1

                if age_index==-1:
                    age_sec=0
                else:
                    age_sec=int(cache_list[age_index+1])

                cache_validity += age_sec

            sql = '''INSERT INTO CACHE (
                REQUEST_METHOD,
                REQUEST_PATH,
                REQUEST_PROTOCOL,
                REQUEST_HEADERS,
                REQUEST_BODY,
                RESPONSE_STATUS_CODE,
                RESPONSE_STATUS_MESSAGE,
                RESPONSE_PROTOCOL,
                RESPONSE_HEADERS,
                RESPONSE_BODY,
                CACHE_VALIDITY
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

            self.cursor.execute(sql, (
                str(headers_request['method']),
                str(headers_request['path']),
                str(headers_request['protocol']),
                json.dumps(headers_request, ensure_ascii=False),
                sqlite3.Binary(body_request),
                str(headers_response['status_code']),
                str(headers_response['status_message']),
                str(headers_response['protocol']),
                json.dumps(headers_response, ensure_ascii=False),
                sqlite3.Binary(body_response),
                str(cache_validity)
            ))

            self.conn.commit()
            Log("Cache - Data stored in cache DB")
        except Exception, e:
            Log('Cache Error - on insert cache: ' + e.message)

    def there_is_cache(self, _request):
        try:
            headers_request, body_request = Parser().http_to_dict(_request)

            sql = '''SELECT
                    ID,
                    RESPONSE_HEADERS,
                    RESPONSE_BODY,
                    CACHE_VALIDITY
                FROM CACHE
                WHERE
                    REQUEST_METHOD=? AND
                    REQUEST_PATH=? AND
                    REQUEST_PROTOCOL=? AND
                    REQUEST_BODY=?  
            '''
            self.cursor.execute(sql, (
                headers_request['method'],
                headers_request['path'],
                headers_request['protocol'],
                body_request,
            ))
            cache = self.cursor.fetchone()
            if cache is None:
                has = False
                cache = ''
            elif cache[3] < gmtime():
                sql = '''
                    DELETE
                    FROM CACHE
                    WHERE ID=?
                '''
                self.cursor.execute(sql, (cache[0],))
                self.conn.commit()
                Log('Cache - cache deleted')
                has = False
                cache = ''
            else:
                has = True
                cache = Parser().dict_to_http(json.JSONDecoder(cache[1], cache[2]))

            return has, cache
        except Exception, e:
            Log('Cache Error - on verify cache: ' + e.message)
            return False, ''
