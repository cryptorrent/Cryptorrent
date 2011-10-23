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


from subprocess import Popen, PIPE

def make_key():
    p = Popen(['openssl', 'genrsa', '-out', 'key.pem', '2048'])
    p.communicate()
    Popen(['openssl', 'rsa', '-in', 'key.pem', '-pubout', '-out',
           'pub-key.pem'])

def encrypt(data, pubkey):
    start = 0
    block_sz = 244
    result = []
    fout = open("/tmp/pub-key.pem", 'w')
    fout.write(pubkey)
    fout.close()
    while start < len(data) - 1:
        block = data[start:start + block_sz]
        p = Popen(['openssl', 'rsautl', '-encrypt', '-inkey',
                   '/tmp/pub-key.pem', '-pubin'], stdin=PIPE, stdout=PIPE)
        out, err = p.communicate(block)
        result.append(out)
        start += block_sz
    return ''.join(result)

def decrypt(data):
    start = 0
    block_sz = 256
    result = []
    while start < len(data) - 1:
        block = data[start: start + block_sz]
        p = Popen(['openssl', 'rsautl', '-decrypt', '-inkey',
                   'key.pem'], stdin=PIPE, stdout=PIPE)
        out, err = p.communicate(block)
        result.append(out)
        start += block_sz
    return ''.join(result)

def rand_string():
    import random
    import string
    s = ""
    for i in xrange(1, random.randrange(1, 5)):
        s += random.choice(string.lowercase)
    s *= random.randint(2, 124)
    return s


if __name__ == "__main__":
    for i in xrange(1000):
        s = rand_string()
        e = encrypt(s)
        r = decrypt(e)
        assert s != e and e != r and s == e
