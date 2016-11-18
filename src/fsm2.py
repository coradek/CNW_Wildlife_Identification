
import numpy as np
import pandas as pd

import sklearn
# from sklearn import cross_validation
# from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import cross_val_score

import src.data_pipeline as dpl

#TODO: this needs to take features and create a model
#  the model needs to be pickled (and saved as current_model)
#  this will then be used by predict_one.py

def label_img_list(df):
    'returns list of image file paths and list of labels'

    #FIXME: rework hard coding
    # raw_df = pd.read_csv('data/FirstStupidModel/metadata.csv')
    # df = raw_df

    df.loc[df.keywords == '[]', 'keywords'] = "not_provided"

    d1 = {'ungulate':["[u'mule deer']", "[u'White-tailed deer']", "[u'elk']"],
          'feline':["[u'bobcat']", "[u'Canada lynx']"],
          'hare':["[u'snowshoe hare']"],
          'canine':["[u'coyote']", "[u'domestic dog']"],
          'small': ["[u'mouse']", "[u'red squirrel']", "[u'Robin']",
                     "[u'bird']", "[u'northern flying squirrel']",
                     "[u'Squirrel (unidentified)']", "[u'chipmunk']", "[u'Squirrel']"],
          'other':["[u'unidentified']", "[u'Camera Check']", "[u'striped skunk']",
                   "[u'Wolverine']", "not_provided", "[u'cougar']"]}

    d2 = {}
    for key,value in d1.iteritems():
        for item in value:
            d2[item] = key


    labels = df.keywords.map(d2)
    image_list = df.file_path

    F = features[(labels != 'hare').values]
    L = labels[labels!='hare']

    # return labels, image_list
    return F,L

def create_model(model_name, photo_dir):
    # ? path_to = dpl.path_dict(model_name, photo_dir = photo_dir)
