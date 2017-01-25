import os
import sys
import hashlib
from collections import defaultdict
import struct


def _hash_jpeg(fh):
    # thank you stack overflow (with minor edits):
    # http://stackoverflow.com/questions/10075065/compute-hash-of-only-the-core-image-data-excluding-metadata-for-an-image
    _hash =  hashlib.sha1()
    # _hash = hashlib.md5()
    assert fh.read(2) == "\xff\xd8"
    while True:
        marker,length = struct.unpack(">2H", fh.read(4))
        assert marker & 0xff00 == 0xff00
        if marker == 0xFFDA: # Start of stream
            _hash.update(fh.read())
            break
        else:
            fh.seek(length-2, os.SEEK_CUR)
    return _hash.hexdigest()

def printhash(file_path):
    with open(file_path) as fh:
        print _hash_jpeg(fh)

def find_duplicates(directory):
    # return a list of lists of duplicates
    duplicate_dict = defaultdict(list)
    count = 0
    for p, dirs, files in os.walk(directory):
        for ff in files:
            # check for .jpg file extension
            # check for wierd non-jpg files (created by picasa?)
            # -> filenames starting with '._'
            if ff[-4:].lower() == '.jpg' and ff[:2] != '._':
                count +=1
                if count % 100 == 0:
                    print "processing file: ", ff
                file_path = os.path.join(p,ff)
                with open(file_path) as fh:
                    duplicate_dict[_hash_jpeg(fh)].append(file_path)
    return [v for v in duplicate_dict.itervalues() if len(v) > 1]
