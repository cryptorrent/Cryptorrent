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


import os
from glob import glob
import cStringIO
import binascii
import zlib

class FileManager:
    file_write_progress = {}
    cached_chunks = {}

    def find_chunk(self, file_name, start_byte_number, end_byte_number):
        f = open(file_name, 'rb')
        ignore_bytes = f.read(start_byte_number)
        bytes_to_read = f.read(end_byte_number - start_byte_number)
        #return zlib.compress(bytes_to_read, 9)
        return bytes_to_read

    def uncompress_chunk(self, compressed_chunk):
        #return zlib.decompress(compressed_chunk)
        return compressed_chunk
    
    def find_file(self, file_name):
        # Check if the file_name exists in our current directory
        path = glob(file_name)
        if path:
            return os.path.getsize(file_name)
        else:
            return None

    def receive_chunk(self, file_name, start_byte, finish_byte, chunk):
        if file_name not in self.file_write_progress:
            self.file_write_progress[file_name] = 0
        progress = self.file_write_progress[file_name]
        if start_byte == progress:
            f = open(file_name, "ab")
            f.write(chunk)
            print "writing chunk starting at %s" % progress
            progress = finish_byte + 1
            while ((file_name, progress) in self.cached_chunks):
                print "writing chunk starting at %s from cached" % progress 
                c = self.cached_chunks[(file_name, progress)]
                f.write(c[0])
                del self.cached_chunks[(file_name, progress)]
                progress = c[1] + 1
            f.close()
        else:
            self.cached_chunks[(file_name, start_byte)] = (chunk, finish_byte)
        self.file_write_progress[file_name] = progress
        
if __name__ == "__main__":
    f = FileManager()
    chunk = f.find_chunk("tozip.txt", 0, 512)
    chunk = f.uncompress_chunk(chunk)
    print chunk

# a = Find_Chunk()
# compressed_chunk = a.find_chunk('test.txt', 1, 3)
# a.uncompress_chunk(compressed_chunk)
