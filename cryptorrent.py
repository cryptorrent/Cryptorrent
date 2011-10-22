import time
import encryption
import rsa
from bootstrap import Bootstrapper
from gossip import GossipServer

#encryption.make_key()
#f = open('pub-key.pem', 'r')

pubkey, privkey = rsa.newkeys(1024)


bs = Bootstrapper(pubkey)
bs.bootstrap()

time.sleep(5)

gs = GossipServer(bs, pubkey, privkey)

while True:
    filename = raw_input('Filename: ')
    if filename == 'exit':
        exit()
    gs.init_file_request(filename)
    
