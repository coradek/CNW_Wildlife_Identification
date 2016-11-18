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
# Refactor to use mongoDB for greater stability
#   if build_json_database fails partway through
#   could end up with broken json file

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
            if ff[-4:].upper() == '.JPG':
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

    # FIXME: file_path not applicable when downloading photo from S3
    if source == 'local':
        dd['file_path'] = photo

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
def Mdata_to_json(photo, outfile, k, with_comma = False):
    '''Turn metadata python dictionary to json'''
    ## add error "please specify write ('w')
    #  or append ('a')" if k is not 'a' or 'w':

    M_dict = build_dictionary(photo)
    with open(outfile, k) as outf:
        json.dump(M_dict, outf, indent = 4)
        if with_comma:
            outf.write(',')

# feed metadata into json file
def build_json_database(directory, f_name):
    # build in warning incase f_name already exists?
    '''
    Returns json database of metadata for
    all photos in the given directory
    and its subdirectories
    '''

    #FIXME: hacky way to get model_path
    # will only work when f_name = model_path + 'raw_metadata.json'
    # which, conveniently, is what happens when using data_pipeline.py
    model_path = f_name[:-17]

    # Open json file
    with open(f_name,'w') as outf:
        outf.write('[')

    # Walk directory for '.jpg' files
    count = 0
    failed_list = []
    for p, dirs, files in os.walk(directory):
        for ff in files:
            if ff[-4:].upper() == '.JPG':
                count +=1
                # Add metadata to json file
                try:
                    Mdata_to_json(p+'/'+ff, f_name, 'a', with_comma = True)
                except:
                    failed_list.append(p+'/'+ff)
                print count-(count%10)
    # Close json list
    with open(f_name,'a') as outf:
        outf.seek(-1, os.SEEK_END)
        outf.truncate()
        outf.write(']')
    print len(failed_list), "photos failed to process"
    with open(model_path + '/fail_log.txt', 'w') as fail_log:
        for item in failed_list:
            fail_log.write(item+'\n')



#INPROGRESS
# This class has adapts the above methods for use with an s3 bucket and MongoDB for greater scalability and stability
class aws(object):
    """handle metadata for photos stored on S3"""
    def __init__(self, bucket):
        self.s3 = boto3.resource('s3')
        self.client = self.s3.meta.client
        self.bucket_name = bucket
        self.photo_bucket = self.s3.Bucket(bucket)

        # this may be a very big list -
        # better way to get photos?
        self.photo_list = list(self.photo_bucket.objects.all())
        self.photo_address = None


    def build_dictionary(self, photo, field_set = None):
        dd = build_dictionary(photo, field_set = field_set, source = 's3')
        dd['photo_address'] = self.photo_address
        return dd


    # Replace with mdata_to_MongoDB
    def Mdata_to_mongo(self, photo, outfile, k):
        '''Turn metadata python dictionary to json'''
        ## add error "please specify write ('w')
        #  or append ('a')" if k is not 'a' or 'w':
        M_dict = self.build_dictionary(photo)
        with open(outfile, k) as outf:
            json.dump(M_dict, outf, indent = 4)


    # rework to take advantage of S3
    # Use MongoDB instead of json for stability
    def build_mongo_database(self, f_name):

        pass


    def upload(self, a_file, key = None):
        '''Uploads files to s3'''

        # Automate transfer of photos to S3

        # currently done outside of python module
        # through ssh to ec2 instance
        pass

if __name__ == '__main__':

    pass
