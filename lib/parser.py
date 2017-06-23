from log import Log
class Parser:
    def __init__(self):
        pass

    def http_to_dict(self, _raw_http):
        lines = _raw_http.split('\n')
        try:
            body_position = lines.index('\r')+1
            b = ''.join(lines[body_position:])
            del lines[body_position - 1:]
        except Exception, e:
            b = ''


        # print lines
        lines = [l.replace('\r', '') for l in lines]
        first_line = lines[0].split(' ')
        d = {}
        if 'HTTP/' in first_line[0]:
            try:
                d['type'] = 'response'
                d['protocol'] = first_line[0]
                d['status_code'] = first_line[1]
                d['status_message'] = ' '.join(first_line[2:])
            except Exception, e:
                Log('Parser Error - error on HTTP response: '+e.message)

        else: # ('GET' or 'HEAD' or 'POST' or 'PUT' or 'DELETE' or 'CONNECT' or 'OPTIONS' or 'TRACE') in first_line[0]:
            try:
                d['type'] = 'request'
                d['method'] = first_line[0]
                d['path'] = first_line[1]
                d['protocol'] = first_line[2]
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
            d[l[0]] = ': '.join(l[1:])

        return d, b

    def dict_to_http(self, _dict, _body):

        if _dict['type'] == 'response':
            s = ' '.join(_dict['protocol'], _dict['status_code'], _dict['status_message']) + '\r\n'
            _dict.pop('protocol')
            _dict.pop('status_code')
            _dict.pop('status_message')
        else:
            s = ' '.join(_dict['method'], _dict['path'], _dict['protocol']) + '\r\n'
            _dict.pop('method')
            _dict.pop('path')
            _dict.pop('protocol')

        _dict.pop('type')

        for k in _dict:
            s += ': '.join(k, _dict[k]) + '\r\n'

        s += '\r\n' + _body

        return s

    def body_length(self,_raw_http):
        d=self.http_to_dict(_raw_http)

        if d['Content-Length']:
            return int(d['Content-Length'])
        else:
            return 0