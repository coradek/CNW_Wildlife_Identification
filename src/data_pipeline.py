from sys import argv
from os.path import isdir
from os import makedirs

import metadata_handler as mdh
import clean_db as cdb
import feature_extractor as fe


def confirm_overwrite(path):
    response = raw_input('This data set already exists. Overwrite? [yes/no] ')
    if response.lower() == 'no':
        return False
    elif response.lower() == 'yes':
        return True
    else:
        print 'please type "yes" or "no"'
        return confirm_overwrite(path)

class DataManager(object):
    """DataManager provides an interface to the project dataset
    It allows dataset creation through the process_photos()
    and loading of datasets which already exist"""

    def __init__(self, photo_dir = None, dataset_name = 'Wildlife_ID_Data'):
        self.photos = photo_dir
        self.data_name = dataset_name
        self.data_path = self._make_path('')
        self.json = self._make_path('raw_metadata.json')
        self.csv = self._make_path('metadata.csv')
        self.features = self._make_path('features.npy')
        self.info = self._make_path('info.txt')


    def _make_path(self, target):
        return "data/{}/{}".format(self.data_name, target)


    def record_info(self):
        #TODO: add date created
        info = 'Data Set Name: '+self.data_name\
                +'\n\tdataset loc: '+self.data_path\
                +'\n\tsource photos: '+self.photos\
                +'\n\tjson data: '+self.json\
                +'\n\tdataframe csv: '+self.csv\

        with open(self.info,'w') as outf:
            outf.write(info)


    #TODO: now that I've pulled out these two functions they look kinda silly
#  Why wrap a function I built elsewhere + one line of text
    def create_json(self):
        mdh.build_json_database(self.photos, self.json)
        print '\ndata pipeline created: {}\n'\
                .format(self.json)


    def create_dataframe(self):
        df = cdb.create_csv(self.json, self.csv)
        print '\ndata pipeline created: {}\n'\
                .format(self.csv)
        return df


    def feature_df(self):
        '''Returns a dataframe of filenames and tensorflow features'''
        df = fe.feature_df(self.csv, self.features)
        return df


    def process_photos(self):
        '''Retrieves metadata from all images in a directory or nested directory of photos.
        Also creates record of dataset structure; creates json file, csv, and numpy array of Inception-v3 features.'''

        if isdir(self.data_path):
            if confirm_overwrite(self.data_path) == False:
                print "aborting process_photos"
                return
            else: pass

        else:
            print 'Creating Directory: '+self.data_path
            makedirs(self.data_path)

        print "\ndata pipeline: fetching  photo metadata, creating pandas database and csv . . .\n"

        self.record_info()

        self.create_json()

        df = self.create_dataframe()

        print "\ndata pipeline: extracting features . . .\n"
        features = fe.extract_features(df,
                                save_loc = self.features[:-4])

        print "\ndata pipeline: photo processing complete!\n"

        # df = fe.feature_df(df, features)
        # return df


if __name__ == '__main__':

    if len(argv)==3:
        ImageProcessor(photo_dir = argv[1], dataset_name = argv[2]).process_photos()

    else:
        ImageProcessor(photo_dir = argv[1]).process_photos()
