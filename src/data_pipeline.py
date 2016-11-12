import metadata_handler as mdh
import clean_db as cdb
from sys import argv

''' run to prepare photos for use in CNN
to use from command prompt:
    python setup.py <'s3' or 'local'> <bucket or directory>
example: python src/setup.py s3 cnwphotos
    python local my_photos'''

def main():

    # Create raw_metadata.json
    if argv[1] == 's3':
        MDH = mdh.aws(argv[2])
        MDH.build_json_database('data/raw_metadata.json')

    if argv[1] == 'local':
        mdh.build_json_database(argv[2], 'data/raw_metadata.json')

    # Create metadata.csv
    df = cdb.process_data('data/raw_metadata.json')
    df.to_csv('data/metadata.csv')

    # Create (the actual df I feed to the CNN)
    # df = FINAL STEP: run through spark get fully preped dataframe


if __name__ == '__main__':

    main()
