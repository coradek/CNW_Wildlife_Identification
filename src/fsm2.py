
import numpy as np
import pandas as pd

import sklearn
# from sklearn import cross_validation
# from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

import src.data_pipeline as dpl

#TODO: this needs to take features and create a model
#  the model needs to be pickled (and saved as current_model)
#  this will then be used by predict_one.py

def prep_data(dataset, drop_hare = True, drop_blank = False):
    # open dataframe of labels and features
    df = dpl.load_df(dataset)

    # choose the parts I need
    d1 = {'Ungulate':["[u'mule deer']", "[u'White-tailed deer']", "[u'elk']"],
          'Feline':["[u'bobcat']", "[u'Canada lynx']",
                    "[u'cougar']", "[u'mountain lion']"],
          'Hare':["[u'snowshoe hare']"],
          'Canine':["[u'coyote']", "[u'domestic dog']"],
          'Small': ["[u'mouse']", "[u'red squirrel']", "[u'Robin']",
                     "[u'bird']", "[u'northern flying squirrel']",
                     "[u'Squirrel (unidentified)']",
                     "[u'chipmunk']", "[u'Squirrel']"],
          'Other':["[u'unidentified']", "[u'Camera Check']","[u'sheep']",
                     "[u'hoary marmot']", "[u'striped skunk']", "[u'skunk']",
                     "[u'Wolverine']","[]", "[u'human']", "[u'Black Bear']"]}

    d2 = {}
    for key,value in d1.iteritems():
        for item in value:
            d2[item] = key

    print "Keyword Value Counts: \n",df.keywords.value_counts()

    # Check for blank keywords, drop if desired
    if "[]" in df.keywords.unique():
        blank_count = df.keywords.value_counts()["[]"]
        print '\n{} photos have a blank keyword entries'.format(blank_count)
        if drop_blank:
            print "dropping blank\n"
            df = df[(df.keywords != "[]").values]

    # display missed labels and drop
    labels = df['keywords'].map(d2)
    missed_labels = df['keywords'][labels.isnull()]
    if len(missed_labels) != 0:
        print 'the following labels were missed\n', missed_labels.unique()
        print 'dropping rows with these labels'
        df = df[labels.notnull()]
        labels = labels[labels.notnull()]

    features = df.drop(['keywords', 'file_path'], axis = 1)
    paths = df.file_path

    if drop_hare:
        print '\ndropping "Hare" for balance'
        features = features[(labels != 'Hare').values]
        paths = df.file_path[(labels != 'Hare').values]
        labels = labels[labels!='Hare']

    print "\nFinal Group Count\n", labels.value_counts()
    return features, labels, paths

#create SVC model
def create_SVC():
#     svm = LinearSVC(C=1.0, loss='squared_hinge', penalty='l2',multi_class='ovr')
    svm = SVC(C=1.0, kernel='linear', degree=3, gamma='auto', coef0=0.0, shrinking=True,
              probability=True, tol=0.001, cache_size=200, class_weight=None,
              verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None)

    return svm


# Create RF Model
def create_RF():

    rf = RF(n_estimators=60, criterion='gini', max_depth=200,
          min_samples_split=2, min_samples_leaf=1,
          min_weight_fraction_leaf=0.0, max_features="auto",
          max_leaf_nodes=None, min_impurity_split=1e-07,
          bootstrap=True, oob_score=False, n_jobs=2,
          random_state=None, verbose=0, warm_start=False,
          class_weight=None)

    return rf


# Train model, return model, prediction, probs
#  and unused portion of dataset
def run_fit(model, X, y, test_size = 0.2):
    X_train, X_test, y_train, y_test = train_test_split(X,y,
                                test_size=test_size, random_state=None)
    model = model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    return model, X_test, y_test, y_pred, y_prob


def save_model(model, path_name):
    with open(path_name, 'wb') as handle:
        pickle.dump(model, handle)
