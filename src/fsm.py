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

    # CONSIDER: is this needed if passing df directly from clean_db
    #  w/o writing to csv

    # patchup the dataframe
    df = df.rename(columns = {'Unnamed: 0':'photo_id'})

    #FIXME: add dummies in data_pipline or clean_db to standardize models
    # add dummy cols to dataframe:
    #FIXME FIXME !!! error on dummy handling
    #  was fine when reading df from .csv
    #  (guessing read_csv stringified the list)
    df = pd.concat([df, pd.get_dummies(df.keywords)], axis=1)

    # pandas has trouble splitting on NaN values -> replace with "not_provided"
    df.loc[pd.isnull(df.copyright_notice), 'copyright_notice'] = "not_provided"

    # Drop unneeded columns
    df = df.drop(['by_line', 'caption_abstract',
                  'contact','object_name','sub_location',
                  'supplemental_category','keywords', "[u'camera check']", "[u'marmot']", "[u'deer']"],
                 axis = 1)
    return df


def create_model(photo_dir, dataframe):

    # convert dataframe to graphlab SFrame
    data = gl.SFrame(dataframe)

    # GET IMAGES:
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
    y = data["[u'mule deer']"]

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
        print a,'  ',b,'  ',c[1]


def main(photo_dir, model_name = 'FirstStupidModel'):
    df = prepare_dataframe(photo_dir, model_name = model_name)
    model,X,y = create_model(df)
    run_model(model,X,y)


if __name__ == '__main__':

    main(argv[1])
# Take dir of photos,
