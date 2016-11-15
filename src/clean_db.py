import pandas as pd
import numpy as np
import re
from sys import argv

import metadata_handler as mdh

'''
Take json file created by metadata_handler
return cleaned dataframe
for use in wildlife_id model
cmd terminal usage: clean_db.py <raw_database.json> <destination.csv>
'''

def fix_col_names(db):
    '''Remove " ", "-", "/" from colunm names'''
    dd = {}
    for col in db.columns:
        new_col = col
        new_col = new_col.replace(' ', '_')
        new_col = new_col.replace('-', '_')
        new_col = new_col.replace('/', '_')
        if new_col != col:
            dd[col] = new_col
    db = db.rename(columns = dd)
    return db

def _fix_date(date):
    # remove decimal?
    date = str(date)
    if date == 'nan':
        return None
    else:
        return re.sub('(....)(..)(..)(..)', '\\1-\\2-\\3', date)

def _fix_time(time):
    # remove decimal?
    time = str(time)
    if time == 'nan':
        return None
    elif len(time) == 7:
        return re.sub('(.)(..)(..)(..)', '\\1:\\2:\\3', time)
    else:
        return re.sub('(..)(..)(..)(..)', '\\1:\\2:\\3', time)

def fix_date_and_time(db):
    fix_date = np.vectorize(_fix_date)
    fix_time = np.vectorize(_fix_time)

    db.date_created = fix_date(db.date_created)
    db.time_created = fix_time(db.time_created)
    return db

# FIXME: Hard Coded - fix for general purpose model
#  use basename?
def simplify_path(db):
    db.file_path = db.file_path.str.strip('/Volumes/Seagate Backup Plus Drive/CNWPhotos/')
    return db

def add_dummies(db):
        # get dummies from keywords column
        db = pd.concat([db, db.keywords.str.join(sep = ' ')\
                                .str.get_dummies(sep=',')], axis=1)
        return db


def process_data(file_name):
    db = pd.read_json(file_name)
    db = fix_col_names(db)
    db = fix_date_and_time(db)
    db = simplify_path(db)
    db = add_dummies(db)

    return db

def main(raw_json, dest_csv):
    df = process_data(raw_json)
    df.to_csv(dest_csv)
    return df

if __name__ == '__main__':
    # # TEST:
    # db = process_data('data/test_DB.json')
    # print db.head(4).T

    # for real
    main(argv[1], argv[2])

    # for arg in argv:
    #     print arg
