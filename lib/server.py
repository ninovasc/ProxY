import socket, sys
from thread import *

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

            print("Server Started Sucessfully [ %d ]\n" % (self.port))
        except Exception, e:
            print e
            print "Unable to inicialize server"
            sys.exit(2)

        while 1:
            try:
                conn, addr = s.accept()  # Accept Connection From Client Browser
                data = conn.recv(self.buffer_size)  # Receiver Client Data
                start_new_thread(self.conn_string, (conn, data, addr))  # Start a Thread
            except KeyboardInterrupt:
                s.close()
                print "\nProxy Server Shutting Down ..."
                print "Bye, bye..."
                sys.exit(1)

        s.close()

    def conn_string(self, conn, data, addr):
        # client browser request appears here
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

            self.proxy_server(webserver, port, conn, data, addr)
        except Exception, e:
            pass

    def proxy_server(self, webserver, port, conn, data, addr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(data)
            while 1:
                # Read reply or data to from end webserver
                reply = s.recv(self.buffer_size)
                if (len(reply) > 0):
                    conn.send(reply)  # send reply back to client
                    dar = float(len(reply))
                    dar = float(dar / 1024)
                    dar = "%.3s" % (str(dar))
                    dar = "%s KB" % (dar)
                    print "Request Done: %s => %s <=" % (str(addr[0]), str(dar))
                else:
                    break # break connection if receive data fail
            s.close()
            conn.close()

        except socket.error, (value, message):
            print "value: " + value
            print "Message:" + message
            s.close()
            conn.close()
            sys.exit(1)