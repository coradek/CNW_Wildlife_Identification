from sys import argv

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

    #FIXME: check if dir exists - if true, confirm overwrite.
    #  Add make dir <dataset_name>

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
    dd['features'] = _make_path('features')

    return dd


def process_photos(photo_dir, dataset_name = 'Wildlife_ID_Data'):
    # TODO:
    # check for dir -
    # create dir
    # (make sure its all saved someplace)

    path_to = path_dict(dataset_name, photo_dir)

    print "\ndata pipeline: fetching  photo metadata, creating pandas database and csv . . .\n"
    df = create_dataframe(photo_dir, dataset_name = dataset_name)
    print "\ndata pipeline: extracting features . . .\n"

    #FIXME: ? is it better to import pandas here and just pass
    #  df.file_path to fe ?

    ftrs = fe.extract_features(df, save_loc = path_to['features'])
    print "\ndata pipeline: photo processing complete!\n"
    return df,ftrs


#TODO:  convert dpl to class
class ImageProcessor(object):
    """docstring for ."""

    def __init__(self, photo_dir, dataset_name = 'Wildlife_ID_Data'):
        self.photo_path = photo_dir
        self.data_path = _make_path('')
        self.json = _make_path('raw_metadata.json')
        self.csv = _make_path('metadata.csv')


    def _make_path(self, target):
        return "data/{}/{}".format(dataset_name, target)



if __name__ == '__main__':

    if argv[2]:
        process_photos(argv[1], dataset_name = argv[2])

    else:
        process_photos(argv[1])
