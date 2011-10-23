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


"""
Bootstrapping process is as follows
1. Listen on multicast address
2. Multicast your IP address, listen for responses (IP addresses of other nodes)
3. Store responses
**4. If no responses, contact main server for list of nodes
**5. Receive list of nodes from main server
**6. If no other nodes, try again later

** Currently Disabled
"""

import json
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import time, datetime, signal, socket
from urllib2 import urlopen
#from threading import Thread
import threading

signal.signal(signal.SIGINT,signal.SIG_DFL)


##########
# SERVER #
##########

class MulticastServerUDP(DatagramProtocol):

    def __init__(self, pkey):
        self.pkey = pkey

    def startProtocol(self):
        print 'Multicast Server Started Listening....'
        # Join a specific multicast group, which is the IP we will respond to
        self.transport.joinGroup('224.0.1.123')

    def datagramReceived(self, datagram, address):
        ip, pkey = datagram.split(None, 1)
        if ip != Bootstrapper.myip:
            Bootstrapper.hosts[ip] = pkey
            print "Bootstrap Server Hosts:....", Bootstrapper.hosts
            print "Heard Multicast Datagram:", repr(ip)
            self.transport.write("%s %s" % (Bootstrapper.myip, self.pkey), address)

class MulticastServerThread(threading.Thread):

    def __init__(self, pkey):
        threading.Thread.__init__(self)
        self.pkey = pkey

    def run(self):
        reactor.listenMulticast(8005, MulticastServerUDP(self.pkey))
        #reactor.run(installSignalHandlers=0)

##########
# CLIENT #
##########

class MulticastClientUDP(DatagramProtocol):

    def datagramReceived(self, datagram, address):
        ip, pkey = datagram.split()
        if ip != Bootstrapper.myip:
            Bootstrapper.hosts[ip] = pkey

class MulticastClientThread(threading.Thread):
    def __init__(self, pkey):
        threading.Thread.__init__(self)
        self.pkey = pkey

    def run(self):
        print "sending multicast hello"
        # Send multicast on 224.0.1.123:8005, on our dynamically allocated port
        reactor.listenUDP(0, MulticastClientUDP()).write("%s %s" % (Bootstrapper.myip, self.pkey), ('224.0.1.123', 8005))

##########
# BACKUP #
##########

HOST = '172.23.124.59'
PORT = 8007

class BackupClientThread(threading.Thread):

    def __init__(self, pkey):
        threading.Thread.__init__(self)
        self.pkey = pkey

    def run(self):
        print "No clients located, attempting to contact backup server...."
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #try:
            s.connect((HOST, PORT))
            s.send("GIMMEHOSTS %s" % self.pkey)
            data = ''

            while True:
                x = s.recv(2048)
                if x[-1] == '}':
                    data += x
                    break
                data += x
            data = json.loads(data)

            for datum in data:
                if datum != Bootstrapper.myip:
                    Bootstrapper.hosts[datum] = data[datum]
            #except Exception as e:
            #    print "Home server is not available at this time: ", e, HOST, PORT
            #    break
            #print "Hosts received from backup server:", Bootstrapper.hosts
            time.sleep(2)

######################
### INITIALIZATION ###
######################

class Bootstrapper:
    hosts = {}
    #myip = urlopen('http://whatismyip.org/').read()
    myip = socket.gethostbyname(socket.gethostname())

    def __init__(self, pkey):
        self.pkey = pkey
        print "BOOTSTRAP IP", Bootstrapper.myip


    def bootstrap(self):
        MulticastServerThread(self.pkey).start()
        MulticastClientThread(self.pkey).start()
        #Give multicast a chance to find some friends
        time.sleep(5)
        if len(self.hosts)==0:
            BackupClientThread(self.pkey).start()

if __name__ == "__main__":
    b = Bootstrapper(1337)
    b.bootstrap()
