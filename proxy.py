import sys
import json
from lib.server import Server
from lib.setup import Setup
from lib.log import Log


if __name__ == '__main__':
    try:
        setup=Setup()
        cfg=setup.config
        msg = "ProxY port load from file, listening on "+ cfg['port']
        Log(msg)
        print msg
        server = Server(int(cfg['port']))
        server.start()
    except KeyboardInterrupt:
        print "\nUser Requested An Interrupt"
        print "ProxY Exiting..."
        sys.exit()
