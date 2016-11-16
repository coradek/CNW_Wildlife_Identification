import metadata_handler as mdh
import clean_db as cdb
from sys import argv

''' run to prepare photos for use in CNN
to use from command prompt:
    python data_pipeline.py <directory of photos> (optional: model_name)'''

def create_dataframe(photo_dir, model_name = 'Wildlife_ID_Model'):

    '''Takes a directory of photos. Returns a dataframe of photo metadata.
    Stores data in raw json and csv form.
    Usage:
    df = dpl.create_dataframe(photo_dir, model_name = <desired_model_name>)
    df can then be customized according to the needs of the individual model
    '''


    #FIXME: check if dir exists - if true, confirm overwrite.
    #  Add make dir <model_name>

    model_path = 'data/' + model_name + '/'

    with open(model_path + 'info.txt','w') as outf:
        outf.write(photo_dir+'\n'+model_path)

    jsonfile = model_path + 'raw_metadata.json'
    csvfile = model_path + 'metadata.csv'
    mdh.build_json_database(photo_dir, jsonfile)
    print '\n', photo_dir,'\n',jsonfile,'\n',csvfile,'\n'
    df = cdb.main(jsonfile, csvfile)
    return df


if __name__ == '__main__':

    if argv[2]:
        create_dataframe(argv[1], model_name = argv[2])

    else:
        create_dataframe(argv[1])
