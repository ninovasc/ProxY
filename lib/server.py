# -*- coding: utf-8 -*-
"""
This module is the proxy server core, here the management of transmission flow is made. 
"""
import socket
import sys
from thread import *
from lib.cache import Cache
from lib.log import Log
from lib.parser import Parser

__docformat__ = 'reStructuredText'


class Server:
    """
    The Server class has five attributes: 
    
    **port** - the server TCP port, brought from config.json file
    **auto_increment_port** - if 'True' the application will try next free port if the **port** is in use
    **do_cache** - if 'True' the application will try use cache
    **max_conn** - the number of simultaneous connections
    **buffer_size** used on receive method to control the TCP flow
    """
    def __init__(self, _port, _auto_increment_port, _cache):

        self.port = _port
        self.auto_increment_port = True if _auto_increment_port == 'True' else False
        self.max_conn = 5  # max connections Queues To Hold
        self.buffer_size = 1000  # Max socket Buffer Size
        self.do_cache = True if _cache == 'True' else False

    def start(self):
        """
        This method inicialize the server and start listening requests.
        """

        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # inicialize Socket
                s.bind(('', self.port))  # bind socket for listen
                s.listen(self.max_conn)  # Start listen for incomming connections
                msg = "ProxY Started Sucessfully [ %d ]" % self.port
                Log(msg)
                print msg
                break
            except Exception, e:
                print e
                msg = "Unable to initialize server on [ %d ]" % self.port
                Log(msg)
                print msg
                if self.auto_increment_port:
                    self.port += 1
                else:
                    sys.exit(2)

        while 1:
            try:
                conn, addr = s.accept()
                data = self.recvall(conn)
                start_new_thread(self.conn_string, (conn, data, addr))  # Start a Thread
            except KeyboardInterrupt:
                s.close()
                print "\nProxY Shutting Down ..."
                print "Bye, bye..."
                sys.exit(1)

        s.close()

    def conn_string(self, conn, data, addr):
        """
        This method is called when a request is received form server listening. This works de request message and
        pass the message to receiver.
        
        :param conn: connection socket
        :param data: request data 
        :param addr: socket address
        """
        request, b = Parser().http_to_dict(data)
        if self.do_cache:
            has, cache = Cache().there_is_cache(data)
        else:
            has = False
            cache = ''

        if not has:
            try:
                url = request['path']
                http_pos = url.find("://")  # find the position of ://
                if http_pos == -1:
                    temp = url
                else:
                    temp = url[(http_pos + 3):]  # get the rest of the url

                port_pos = temp.find(":")  # find the port if any
                webserver_pos = temp.find("/")  # find the end of the web server

                if webserver_pos == -1:
                    webserver_pos = len(temp)

                if port_pos == -1 or webserver_pos < port_pos:
                    # default port
                    port = 80
                    webserver = temp[:webserver_pos]
                else:
                    # specific port
                    port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                    webserver = temp[:port_pos]

                self.proxy_server(webserver, port, conn, data, addr)
            except Exception, e:
                print e
                pass
        else:
            Log('Cache was used')
            conn.send(cache)
            conn.close()

    def proxy_server(self, webserver, port, conn, data, addr):
        """
        This method receive the request of **conn_string** method and sends to this destination. After receive
        the response return this to client.
        
        :param webserver: host
        :param port: hosts port
        :param conn: connection socket
        :param data: request (HTTP message)
        :param addr: socket address
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(data)
            while 1:

                reply = self.recvall(s)

                if len(reply) > 0:
                    # Parser().http_to_dict(reply)
                    # Log(reply)
                    if self.do_cache:
                        Cache().store_cache(data, reply)
                    conn.send(reply)  # send reply back to client
                    Log('response received!')
                else:
                    break  # break connection if receive data fail
            s.close()
            conn.close()

        except socket.error, (value, message):
            print "value: " + value
            print "Message:" + message
            s.close()
            conn.close()
            sys.exit(1)

    def recvall_old(self, sock):
        """
        Deprectaed method to receive data Based on **Contend-Length** HTTP header parameter.
        
        :param sock: socket
        :return: received data
        """
        data = ""
        # while True:
        part = sock.recv(self.buffer_size)
        if part != '':
            d, b = Parser().http_to_dict(part)
            data += part
            part = sock.recv(int(d['Content-Length']))
            data += part
            # if part < BUFF_SIZE:
            # either 0 or end of data
            # break
            return data
        else:
            return data

    def recvall(self, sock):
        """
        This method receive all data from TCP socke based on Server **bufer_size**.
        
        :param sock: socket
        :return: received data
        """
        data = ''
        while True:
            part = sock.recv(self.buffer_size)
            data += part
            if len(part) < self.buffer_size:
                break

        return data
