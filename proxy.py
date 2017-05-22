import sys
from lib.server import Server


if __name__ == '__main__':
    try:
        listening_port = int(raw_input("[*] Enter Port Number for ProxY server: "))
        server = Server(listening_port)
        server.start()
    except KeyboardInterrupt:
        print "\nUser Requested An Interrupt"
        print "Application Exiting..."
        sys.exit()