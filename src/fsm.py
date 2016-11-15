from sys import argv
import pandas as pd
import numpy as np
import graphlab as gl
from sklearn.linear_model import LogisticRegression as LR

# import src.metadata_handler as mdh
# import src.clean_db as cdb
import src.data_pipeline as dpl

'''a logistic regression model predicting presence of mule deer in a remote camera image'''

def prepare_dataframe(photo_dir, model_name = 'FirstStupidModel'):

    '''customize dataframe for FSM from dir of photos'''

    df = dpl.create_dataframe(photo_dir, model_name = 'FirstStupidModel')

    # patchup the dataframe if read from csv
    df = df.rename(columns = {'Unnamed: 0':'photo_id'})

    df.loc[pd.isnull(df.copyright_notice), 'copyright_notice'] = "not_provided"

    # Drop unneeded columns
    df = df.drop(['by_line', 'caption_abstract',
                  'contact','object_name','sub_location',
                  'supplemental_category','keywords'],
                 axis = 1)

    # Drop improper classifications

    # FIXME: better to remove cols NOT IN list of proper classifiers
    # FIXME: should drop rows which are clasified poorly
    #  CONSIDER: adding "bad_classification" column
    #  or "remove=true"
    #  Any bad data entry could then have val set to true
    #  then remove all bad rows at once

    bad_classifications = ["camera check", "marmot", "deer"]
    df = df.drop(bad_classifications, axis = 1)


    return df


def create_model(photo_dir, dataframe):

    # convert dataframe to graphlab SFrame
    data = gl.SFrame(dataframe)

    # GET IMAGES:
    # FIXME: currently relies on graphlab underlying structure
    #  to associate photos with proper rows
    #  SHOULD AT LEAST CHECK photos match
    img_sframe = gl.image_analysis.load_images(photo_dir,
                            "auto", with_path=False,
                            recursive=True)

    # ADD IMAGES TO data
    data.add_column(img_sframe['image'], name='image')

    # Filter for desired rows ('copyright_notice' == 'Conservation Northwest')
    data = data[data['copyright_notice'] == 'Conservation Northwest']

    # Get Imagenet pretrained CNN
    imagenet_model = gl.load_model('https://static.turi.com/products/graphlab-create\
                                            /resources/models/python2.7/imagenet_model_iter45')
    # Convert photos to proper size for imagenet
    data['image'] = gl.image_analysis.resize(data['image'], 256, 256, 3, decode=True)

    # Get features from CNN
    data['imagenet_features'] = imagenet_model.extract_features(data)

    # CREATE FSM!!!
    log_regr = LR(penalty='l2', dual=False, tol=0.0001, C=1.0,
               fit_intercept=True, intercept_scaling=1,
               class_weight=None, random_state=None, solver='liblinear',
               max_iter=100, multi_class='ovr', verbose=0,
               warm_start=False, n_jobs=2)

    X = data['imagenet_features']
    y = data["mule deer"]

    # fit model to data
    model = log_regr.fit(X,y)

    # X and y added to allow run_model
    # to run on training set without re-processing
    return model,X,y



def run_model(model, X, y):
    # originally built to test model on same photos
    # should run on dif photo set

    # fit model to data
    model = model.fit(X,y)
    pred = model.predict(X)
    prob = model.predict_proba(X)
    print'true | pred | prob [mule deer = true]'
    for a,b,c in zip(y, pred, prob):
        print ' ',a,'  ',b,'   ',c[1]


def main(photo_dir, model_name = 'FirstStupidModel'):
    df = prepare_dataframe(photo_dir, model_name = model_name)
    model,X,y = create_model(photo_dir, df)
    run_model(model,X,y)


if __name__ == '__main__':

    main(argv[1])
# Take dir of photos,
