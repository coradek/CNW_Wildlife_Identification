from sys import argv
import os
import pandas as pd
import numpy as np
import graphlab as gl
from graphlab.toolkits.cross_validation import shuffle
from sklearn.linear_model import LogisticRegression as LR
from sklearn.model_selection import cross_val_score


# import src.metadata_handler as mdh
# import src.clean_db as cdb
import src.data_pipeline as dpl

'''a logistic regression model predicting presence of White-tailed deer in images from data/second_sample'''

def local_imagenet():
    # FIXME: Save a local copy of the imagenet CNN to reduce load time

    # Get Imagenet pretrained CNN
    imagenet_model = gl.load_model('https://static.turi.com/products/graphlab-create\
                                            /resources/models/python2.7/imagenet_model_iter45')

    pass

def balance_deer(SF):

    deer_sf = SF[SF['White-tailed deer']==1]

    other_sf, _ = SF[SF['White-tailed deer']==0].random_split(0.09, seed=42)

    bal_sf = deer_sf.append(other_sf)

    bal_sf = bal_sf[['file_path','White-tailed deer','imagenet_features']]

    bal_sf = shuffle(bal_sf)

    return bal_sf

def prepare_dataframe(photo_dir, predict_class, model_name = 'FirstStupidModel'):

    #FIXME: Get local copy of imagenet
    # Get Imagenet pretrained CNN
    imagenet_model = gl.load_model('https://static.turi.com/products/graphlab-create\
                    /resources/models/python2.7/imagenet_model_iter45')

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


    # FIXME: remove improper classifications
    # FIXME: remove bad rows

    # Convert dataframe to graphlab SFrame
    data = gl.SFrame(df)

    # GET IMAGES:
    img_sframe = gl.image_analysis.load_images(photo_dir, "auto",
                                                with_path=True, recursive=True)

    # ADD IMAGES to SFrame
    data.add_column(img_sframe['image'], name='image')

    # Convert photos to proper size for imagenet
    data['image'] = gl.image_analysis.resize(data['image'], 256, 256, 3, decode=True)

    # Get features from CNN
    data['imagenet_features'] = imagenet_model.extract_features(data)

    if predict_class == "White-tailed deer":
        data = balance_deer(data)

    # Save SFrame to reduce load time
    data.save('data/' + model_name + '/sframe')

    print "\ndataframe prepared\n"
    return data


def create_model(data, predict_class = "White-tailed deer"):
    '''build model using CNN features
    if default predict_class is used model opperates on balanced dataset'''


    # CREATE FSM!!!
    train_data, test_data = data.random_split(0.9)

    log_regr = LR(penalty='l2', dual=False, tol=0.0001, C=1.0,
               fit_intercept=True, intercept_scaling=1,
               class_weight='balanced', random_state=None, solver='liblinear',
               max_iter=100, multi_class='ovr', verbose=0,
               warm_start=False, n_jobs=2)

    X = list(train_data['imagenet_features'])
    y = list(train_data[predict_class])

    X_test = list(test_data['imagenet_features'])
    y_test = list(test_data[predict_class])

    # fit model to data
    model = log_regr.fit(X,y)


    # FIXME Save model? and test data?
    # X and y added to allow run_model
    # to run on training set without re-processing
    return model,X_test,y_test



def run_model(model, X_test, y_test):
    # Modify for web app (or create new function)
    # to predict one photo
    def crossval(score_type):
        return cross_val_score(model,
                                X_test,
                                y_test,
                                cv = 3,
                                scoring= score_type)

    print model.score(X_test, y_test)
    print "accuracy : ", crossval('accuracy')
    print "precision: ", crossval('precision')
    print "recall   : ", crossval('recall')
    print "- logloss: ", crossval('neg_log_loss')


def main(photo_dir, model_name = 'FirstStupidModel',
                predict_class = "White-tailed deer"):

    # FIXME: Check line 1 of info.txt
    #  to see if saved data matches photo_dir
    if 'sframe' in os.listdir('data/' + model_name + '/'):
        df = gl.load_sframe('data/' + model_name + '/sframe')
    else:
        df = prepare_dataframe(photo_dir,
                             predict_class,
                             model_name = model_name)

    model,X,y = create_model(df, predict_class = predict_class)
    run_model(model,X,y)


if __name__ == '__main__':

    main(argv[1])
# Take dir of photos,
