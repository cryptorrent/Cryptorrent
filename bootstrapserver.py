# This file is part of Cryptorrent.
#
# EXHIBIT A. Common Public Attribution License Version 1.0.
#
#“The contents of this file are subject to the Common Public Attribution License
# Version 1.0 (the “License”); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.opensource.org/licenses/cpal_1.0. The License is based on the Mozilla
# Public License Version 1.1 but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the Original
# Developer. In addition, Exhibit A has been modified to be consistent with Exhibit B.

# Software distributed under the License is distributed on an “AS IS” basis, WITHOUT
# WARRANTY OF ANY KIND, either express or implied. See the License for the specific
# language governing rights and limitations under the License.
# 
# The Original Code is online at https://github.com/cryptorrent/Cryptorrent.
#
# The Original Developer is not the Initial Developer and is __________. If left blank,
# the Original Developer is the Initial Developer.

# The Initial Developers of the Original Code are Joshua Evenson, Lyle Mills, Hoa-Long Tam,
# and Anirudh Todi. All portions of the code written by Joshua Evenson, Lyle Mills, Hoa-Long Tam,
# and Anirudh Todi are Copyright (c) Joshua Evenson, Lyle Mills, Hoa-Long Tam, and Anirudh Todi.
# All Rights Reserved.
#
# Contributor ______________________.
#
# EXHIBIT B. Attribution Information
#
# Attribution Copyright Notice: Copyright © Joshua Evenson, Lyle Mills, Hoa-Long Tam,
# and Anirudh Todi.
# Attribution Phrase: Created by Joshua Evenson, Lyle Mills, Hoa-Long Tam, Anirudh Todi.
#
# Attribution URL: https://github.com/cryptorrent/Cryptorrent
#
# Display of Attribution Information is required in Larger Works which are defined in the
# CPAL as a work which combines Covered Code or portions thereof with code not governed by the terms of the CPAL.




import json
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import time
import datetime
import threading
from threading import Timer
from threading import Thread
import signal

signal.signal(signal.SIGINT,signal.SIG_DFL)

hosts = {}

class LoggingProtocol(LineReceiver):

    def connectionMade(self):
        client = self.transport.getPeer().host
        print "connection from", client #other options are port, type
        

    def dataReceived(self, line):
        client = self.transport.getPeer().host
        print client, "says", line
        linedata = line.split(None, 1)
        t = datetime.datetime.utcnow()
        if client != "127.0.0.1":
            hosts[client] = (linedata[1], time.mktime(t.timetuple()))

        if linedata[0] == "HERE":
            self.transport.write("OK")
        elif linedata[0] == "GIMMEHOSTS":
            print hosts
            to_send = {}
            counter = 0
            for host in hosts:
                counter += 1
                if counter > 10:
                    break
                to_send[host] = hosts[host][0]
            self.transport.write(json.dumps(to_send))
        else:
            self.transport.write("Invalid Message")
        self.factory.fp.write(line+'\n')
        self.factory.fp.flush()


class LogfileFactory(Factory):

    protocol = LoggingProtocol

    def __init__(self, fileName):
        self.file = fileName

    def startFactory(self):
        self.fp = open(self.file, 'a')

    def stopFactory(self):
        self.fp.close()

def runCleanUp():
    bootable = []
    for host in hosts:
        if(hosts[host][1] + TIMEOUT < time.mktime(datetime.datetime.utcnow().timetuple())):
            bootable.append(host)
    for host in bootable:
        del hosts[host]
        print host + " was booted beacuse of a timeout.\n"
    Timer(CLEANUPTIMEINTERVAL,runCleanUp,()).start()
        
class runListener(Thread):
    def run(self):
        reactor.listenTCP(8007, LogfileFactory("bootstrap.log"))
        print "listening TCP on port 8007"
        reactor.run(installSignalHandlers=0)

runListener().start()

TIMEOUT = 30
CLEANUPTIMEINTERVAL = 2
runCleanUp()


import signal
signal.signal(signal.SIGINT,signal.SIG_DFL)
