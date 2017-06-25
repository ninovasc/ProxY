# -*- coding: utf-8 -*-
"""
Parser module for HTTP messages, convert a data stream to dictionary
and vice-versa.
"""
from log import Log

__docformat__ = 'reStructuredText'


class Parser:
    def __init__(self):
        pass

    def http_to_dict(self, _raw_http):
        """
        An HTTP to dictonary converter.
        
        :param _raw_http: a HTTP message
        :return: **header_params** as dictonary with HTTP header parameters and **body** as HTTP body if exists
        """
        lines = _raw_http.split('\n')
        try:
            body_position = lines.index('\r')+1
            body = ''.join(lines[body_position:])
            del lines[body_position - 1:]
        except Exception, e:
            body = ''


        # print lines
        lines = [l.replace('\r', '') for l in lines]
        first_line = lines[0].split(' ')
        header_params = {}
        if 'HTTP/' in first_line[0]:
            try:
                header_params['type'] = 'response'
                header_params['protocol'] = first_line[0]
                header_params['status_code'] = first_line[1]
                header_params['status_message'] = ' '.join(first_line[2:])
            except Exception, e:
                Log('Parser Error - error on HTTP response: '+e.message)

        else: # ('GET' or 'HEAD' or 'POST' or 'PUT' or 'DELETE' or 'CONNECT' or 'OPTIONS' or 'TRACE') in first_line[0]:
            try:
                header_params['type'] = 'request'
                header_params['method'] = first_line[0]
                header_params['path'] = first_line[1]
                header_params['protocol'] = first_line[2]
            except Exception, e:
                Log('Parser Error - error on HTTP request: ' + e.message)
        # else:
        #     Log('Parser Error - on HTTP not response neither request.')
        #     return None, None

        lines.pop(0)
        for l in lines:
            if ':' not in l:
                break
            l = l.split(': ')
            header_params[l[0]] = ': '.join(l[1:])

        return header_params, body

    def dict_to_http(self, _dict, _body):
        """
        An dictionary to HTTP message converter.
        
        :param _dict: dictonary with HTTP header parameters
        :param _body: data to HTTP body
        :return: an HTTP message
        """
        if _dict['type'] == 'response':
            http_msg = ' '.join(_dict['protocol'], _dict['status_code'], _dict['status_message']) + '\r\n'
            _dict.pop('protocol')
            _dict.pop('status_code')
            _dict.pop('status_message')
        else:
            http_msg = ' '.join(_dict['method'], _dict['path'], _dict['protocol']) + '\r\n'
            _dict.pop('method')
            _dict.pop('path')
            _dict.pop('protocol')

        _dict.pop('type')

        for k in _dict:
            http_msg += ': '.join(k, _dict[k]) + '\r\n'

        http_msg += '\r\n' + _body

        return http_msg

    def body_length(self,_raw_http):
        """
        Measures the lenght of body of HTTP message
        
        :param _raw_http: a HTTP message
        :return: length of HTTP body
        """
        d=self.http_to_dict(_raw_http)

        if d['Content-Length']:
            return int(d['Content-Length'])
        else:
            return 0