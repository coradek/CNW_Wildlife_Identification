import os
from glob import glob
from iptcinfo import IPTCInfo, c_datasets
import json


'''
Process nested directories of photos:
create list of metadata fields
collect metadata from all photos
write to json database
'''

# Transform these functions to class (mdh.local)
# create second class for same functions on s3 (mdh.s3)

def get_fields(directory):

    ''' Find relevant metadata fields:
    walk directories and add numeric keys for
    non-empty meta data fields to field set '''

    # Was also curious to see which fields were occupied

    ## strip '/' only if it is at the end
    #  otherwise it may mess with nested dirs
    #  (e.g. sample/photo/set)
    # directory = directory.strip('/')

    field_set = set()
    for p, dirs, files in os.walk(directory):
        for ff in files:
            if ff[-4:] == '.JPG':
                info = IPTCInfo(directory+'/'+ ff)
                data_dict = dict(info.data)
                fields = set(data_dict.keys())
                field_set = field_set.union(fields)
    return field_set


def build_dictionary(photo, field_set = None, source = 'local'):
    '''
    Get one photo's metadata as a dictionary.
    * Provide field_set to add entries
    for fields found in other photos
    '''

    dd = {}

    # Fix: file_path not applicable when downloading photo from S3
    if source == 'local':
        dd['file_path'] = photo

    #FIX: need some way to referance photos on s3
    if source == 's3':
        dd['file_path'] = 'THE CLOUD'
    info = IPTCInfo(photo)
    data_dict = dict(info.data)

    # return dict with entries for all fields in field_set
    if field_set:
        for k,v in field_set:
            dd[c_datasets[k]].get(v, None)
    # return dict with entries for fields filled in metadata
    else:
        for k,v in data_dict.iteritems():
            dd[c_datasets[k]] = v
    return dd


# write metadata dict to JSON
def Mdata_to_json(photo, outfile, k):
    '''Turn metadata python dictionary to json'''
    ## add error "please specify write ('w')
    #  or append ('a')" if k is not 'a' or 'w':

    M_dict = build_dictionary(photo)
    with open(outfile, k) as outf:
        json.dump(M_dict, outf, indent = 4)



def build_json_database(directory, f_name):
    '''
    Returns json database of metadata for
    all photos the given directory
    and all of its subdirectories
    '''

    # are nested opens bad?
    # Consider: refactor to avoid nested open statements

    with open(f_name,'w') as outf:
        outf.write('[')
    for p, dirs, files in os.walk(directory):
        for ff in files:
            if ff[-4:] == '.JPG':
                Mdata_to_json(p+'/'+ff, f_name, 'a')
                with open(f_name,'a') as outf:
                    outf.write(',')
    with open(f_name,'a') as outf:
        outf.seek(-1, os.SEEK_END)
        outf.truncate()
        outf.write(']')


# write directly to CSV?

# write to SQL?
