"""
**The main module**

Just starts the application. Run "python proxy.py" and configure 
the browser HTTP proxy to server port. By default the port is 12000,
you can change on config.json file, is the port is been used the
next will be try and on.
"""
__docformat__ = 'reStructuredText'

import sys
import json
from lib.server import Server
from lib.setup import Setup
from lib.log import Log

if __name__ == '__main__':

    try:
        setup=Setup()
        cfg=setup.config
        msg = "ProxY port load from file, trying to listening on "+ cfg['port']
        Log(msg)
        print msg
        server = Server(int(cfg['port']), cfg['auto_increment_port'], cfg['cache'])
        server.start()
    except KeyboardInterrupt:
        print "\nUser Requested An Interrupt"
        print "ProxY Exiting..."
        sys.exit()
