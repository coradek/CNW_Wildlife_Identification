import os
import sys
import hashlib
from collections import defaultdict
import struct


def _hash_jpeg(file_path):
    # thank you stack overflow (with minor edits):
    # http://stackoverflow.com/questions/10075065/compute-hash-of-only-the-core-image-data-excluding-metadata-for-an-image
    _hash =  hashlib.sha1()
    # _hash = hashlib.md5()
    with open(file_path) as fh:
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

# TODO: consider refactor to run on list of images (better for dataframe)
#       provide separate funstion to get list from dir
def find_duplicates(directory):
    # return a list containing lists of duplicates
    # [[photo1_a, photo1_b], [photo2_a, photo2_b]]
    duplicate_dict = defaultdict(list)
    count = 0
    for p, dirs, files in os.walk(directory):
        for ff in files:
            # check for .jpg file extension
            # check for wierd non-jpg files (created by picasa?)
            #    -> filenames starting with '._'
            if ff[-4:].lower() == '.jpg' and ff[:2] != '._':
                count +=1
                if count % 100 == 0:
                    print "processing file: ", ff
                file_path = os.path.join(p,ff)
                duplicate_dict[_hash_jpeg(file_path)].append(file_path)
    return [v for v in duplicate_dict.itervalues() if len(v) > 1]


def _flatten(nestedlist):
    return [item for sublist in nestedlist for item in sublist]


def duplicate_flatlist(directory):
    # return a list of all non-unique photos in a given directory
    return _flatten(find_duplicates(directory))
