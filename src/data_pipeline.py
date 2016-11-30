from sys import argv
from os.path import isdir
from os import makedirs

import metadata_handler as mdh
import clean_db as cdb
import feature_extractor as fe


''' takes directory of images (and optional dataset name)
to use from command prompt:
    python data_pipeline.py <directory of photos> (optional: dataset_name)'''


#TODO: separate mdh and cdb steps?
#  paths can then be specified only in process photos
#  get_raw_metadata and create_dataframe can then take paths
#  instead of taking dataset_name and re-creating path names

def get_raw_metadata():
    pass


def create_dataframe(photo_dir, dataset_name = 'Wildlife_ID_Data'):

    '''Takes a directory of photos. Returns a dataframe of photo metadata.
    Stores data in raw json and csv form.
    Usage:
    df = dpl.create_dataframe(photo_dir, dataset_name = <desired_dataset_name>)
    df can then be customized according to the needs of the individual dataset
    '''

    path_to = path_dict(dataset_name, photo_dir)
    data_path = path_to['dataset']

    with open(data_path + 'info.txt','w') as outf:
        outf.write(photo_dir+'\n'+data_path)

    jsonfile = path_to['json']
    csvfile = path_to['csv']
    mdh.build_json_database(photo_dir, jsonfile)
    print '\ndata pipeline processing: {}\ncreated: {}\ncreated: {}\n'\
            .format(photo_dir, jsonfile, csvfile)

    df = cdb.create_csv(jsonfile, csvfile)
    return df


def path_dict(dataset_name, photo_dir = None):
    'returns dict of paths for structure of data folder'
    def _make_path(target):
        return "data/{}/{}".format(dataset_name, target)
    dd = {}
    dd['photos'] = photo_dir
    dd['dataset'] = _make_path('')
    dd['json'] = _make_path('raw_metadata.json')
    dd['csv'] = _make_path('metadata.csv')
    dd['features'] = _make_path('features.npy')

    return dd


def process_photos(photo_dir, dataset_name = 'Wildlife_ID_Data'):

    if isdir('data/'+dataset_name):
        response = raw_input('This data set already exists. Overwrite? [yes/no]')
        if response.lower() == 'no':
            return
        elif response.lower() == 'yes':
            pass
        else:
            print 'yes or no required - aborting'
            return
    else:
        makedirs('data/'+dataset_name)

    path_to = path_dict(dataset_name, photo_dir)

    print "\ndata pipeline: fetching  photo metadata, creating pandas database and csv . . .\n"
    df = create_dataframe(photo_dir, dataset_name = dataset_name)
    print "\ndata pipeline: extracting features . . .\n"

    #TODO: ? is it better to import pandas here and just pass
    #  df.file_path to fe ?

    features = fe.extract_features(df,
                            save_loc = path_to['features'][:-4])
    print "\ndata pipeline: photo processing complete!\n"

    df = fe.feature_df(df, features)

    # return df


# loads a dataframe with only
def load_df(dataset_name):
    path_to = path_dict(dataset_name)
    df = fe.feature_df(path_to['csv'], path_to['features'])
    return df


#TODO:  convert dpl to class
class ImageProcessor(object):
    """docstring for ImageProcessor"""

    def __init__(self, photo_dir, dataset_name = 'Wildlife_ID_Data'):
        self.photos = photo_dir
        self.dataset = _make_path('')
        self.json = _make_path('raw_metadata.json')
        self.csv = _make_path('metadata.csv')
        self.features = _make_path('features')
        self.info = _make_path(info.txt)


    def _make_path(self, target):
        return "data/{}/{}".format(dataset_name, target)

    def record_info():
        #TODO: record file structure/location of data for the give IP object
        pass



if __name__ == '__main__':

    if argv[2]:
        process_photos(argv[1], dataset_name = argv[2])

    else:
        process_photos(argv[1])
