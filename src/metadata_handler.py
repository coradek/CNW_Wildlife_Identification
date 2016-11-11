import os
from glob import glob
from iptcinfo import IPTCInfo, c_datasets
import json
import boto3


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
        dd['photo_address'] = photo

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



def build_json_database(directory, f_name, upload_to = None):
    '''
    Returns json database of metadata for
    all photos the given directory
    and its subdirectories
    (optional upload photos and json to aws S3)
    '''

    if upload_to:
        s3 = boto3.resource('s3')
        photo_bucket = s3.Bucket(upload_to)

    # are nested opens bad?
    # Consider: refactor to avoid nested open statements
    # ? Do I need to close photo after upload

    with open(f_name,'w') as outf:
        outf.write('[')
    for p, dirs, files in os.walk(directory):
        for ff in files:
            if ff[-4:] == '.JPG':
                Mdata_to_json(p+'/'+ff, f_name, 'a')
                if upload_to:
                    photo = open(p+'/'+ff, 'rb')
                    photo_bucket.put_object(Key=p+'/'+ff, Body=photo)
                with open(f_name,'a') as outf:
                    outf.write(',')
    with open(f_name,'a') as outf:
        outf.seek(-1, os.SEEK_END)
        outf.truncate()
        outf.write(']')
    if upload_to:
        jsonDB = open(f_name, 'rb')
        photo_bucket.put_object(Key=f_name, Body=jsonDB)


# write directly to CSV?

# write to SQL?


# This class has adapts the above methods for use with an s3 bucket
class aws(object):
    """handle metadata for photos stored on S3"""
    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.client = self.s3.meta.client
        self.bucket_name = bucket
        self.photo_bucket = self.s3.Bucket(bucket)

        # this may be a very big list -
        # better way to get photos?
        # take 1000 to start
        # change .limit to .all()
        self.photo_list = list(self.photo_bucket.objects.all())
        self.photo_address = None


    def build_dictionary(self, photo, field_set = None):
        dd = build_dictionary(photo, field_set = field_set, source = 's3')
        dd['photo_address'] = self.photo_address
        return dd


    def Mdata_to_json(self, photo, outfile, k):
        '''Turn metadata python dictionary to json'''
        ## add error "please specify write ('w')
        #  or append ('a')" if k is not 'a' or 'w':

        M_dict = self.build_dictionary(photo)
        with open(outfile, k) as outf:
            json.dump(M_dict, outf, indent = 4)


    def build_json_database(self, f_name):
        # build in warning incase f_name already exists?
        with open(f_name,'w') as outf:
            outf.write('[')
        for photo in self.photo_list:
            if photo.key[-4:] == '.JPG':
                self.photo_address = photo.key
                self.client.download_file(self.bucket_name, photo.key, 'data/temp_photo.jpg')
                self.Mdata_to_json('data/temp_photo.jpg', f_name, 'a')
                with open(f_name,'a') as outf:
                    outf.write(',')
                os.remove('data/temp_photo.jpg')
        with open(f_name,'a') as outf:
            outf.seek(-1, os.SEEK_END)
            outf.truncate()
            outf.write(']')

    def upload_photos(directory):
        '''Uploads all .JPG files in directory
        and its subdirectories '''
        for p, dirs, files in os.walk(directory):
            for ff in files:
                if ff[-4:] == '.JPG':
                    # Upload a new file
                    photo = open(p+'/'+ff, 'rb')
                    my_bucket.put_object(Key=p+'/'+ff, Body=photo)


if __name__ == '__main__':

    pass
