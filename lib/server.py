import socket
import sys
from thread import *
from lib.log import Log
from lib.parser import Parser


class Server:
    def __init__(self, _port):
        self.port = _port
        self.max_conn = 5  # max connections Queues To Hold
        self.buffer_size = 4096  # Max socket Buffer Size

    def start(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # inicialize Socket
            s.bind(('', self.port))  # bind socket for listen
            s.listen(self.max_conn)  # Start listen for incomming connections

            print("ProxY Started Sucessfully [ %d ]\n" % self.port)
        except Exception, e:
            print e
            print "Unable to initialize server"
            sys.exit(2)

        while 1:
            try:
                conn, addr = s.accept()  # Accept Connection From Client Browser
                data = conn.recv(self.buffer_size)  # Receiver Client Data
                start_new_thread(self.conn_string, (conn, data, addr))  # Start a Thread
            except KeyboardInterrupt:
                s.close()
                print "\nProxY Shutting Down ..."
                print "Bye, bye..."
                sys.exit(1)

        s.close()

    def conn_string(self, conn, data, addr):
        # client browser request appears here
        Log(data)
        request, b =Parser().http_to_dict(data)
        try:
            first_line = data.split('\n')[0]

            url = first_line.split(' ')[1]

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
            # Parser().http_to_dict(data)

            self.proxy_server(webserver, port, conn, data, addr)
        except Exception, e:
            print e
            pass

    def proxy_server(self, webserver, port, conn, data, addr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(data)
            while 1:
                # Read reply or data to from end webserver

                reply = self.recvall(s) # s.recv(self.buffer_size)

                if len(reply) > 0:
                    # Parser().http_to_dict(reply)
                    Log(reply)
                    #insert cache here
                    conn.send(reply)  # send reply back to client
                    # dar = float(len(reply))
                    # dar = float(dar / 1024)
                    # dar = "%.3s" % str(dar)
                    # dar = "%s KB" % dar
                    # print "Request Done: %s => %s <=" % (str(addr[0]), str(dar))
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

    def recvall(self,sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = ""
        # while True:
        part = sock.recv(BUFF_SIZE)
        if part != '':
            d, b=Parser().http_to_dict(part)
            data+=part
            part=sock.recv(int(d['Content-Length']))

            # print part
            data += part
            print data
                # if part < BUFF_SIZE:
                    # either 0 or end of data
                    # break
            return data
        else:
            return data
