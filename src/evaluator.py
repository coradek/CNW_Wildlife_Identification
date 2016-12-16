from __future__ import division

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cPickle as pickle

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score



def cm_report(labels, y_test, y_pred):
    '''Confusion Matrix Report takes a list of labels for the training set, a test set, and  test set predictions;
    prints a report on value counts and classification percentages
    returns the confusion matrix and 'percentage' matrix'''

    groups = sorted(labels.value_counts().index)
    cm = confusion_matrix(y_test,y_pred, labels = groups)
    alphabetized_counts = np.array([[y_test.value_counts().get(group, default = 0) for group in groups]])

    percent_matrix = cm*100/alphabetized_counts.T
    percent_matrix = percent_matrix.round(decimals = 2)
    percent_matrix = np.nan_to_num(percent_matrix)

    print "Total value counts: \n",labels.value_counts()
    print "\nTest set value counts:\n",y_test.value_counts()
    print "\n"
    for i, grp in enumerate(groups):
        print grp
    print '\nTest Confusion Matrix:\n', cm
    print '\nPercentage True in each predicted class\n', percent_matrix
    print '\n'

    return cm, percent_matrix


def eval_model(model, X_test, y_test):
    '''prints a variety of performance metrics for a griven model'''
    def crossval(score_type):
        try: score = cross_val_score(model, X_test, y_test,
                            cv = 5, scoring= score_type)
        except: score = 'invalid metric'

        return score

    print "accuracy : ", crossval('accuracy')
    print "precision: ", crossval('precision')
    print "recall   : ", crossval('recall')
    print "- logloss: ", crossval('neg_log_loss')


def plot_probs(probs, save_as = None):
    '''plot 'probability' that a given image is in each category'''

    # create ordered DataFrame of categories and probabilities
    groups = ['Canine', 'Feline', 'Other', 'Small', 'Ungulate']
    to_plot = pd.DataFrame(groups, columns = ['groups'])
    to_plot['probs'] = probs[1][0]
    to_plot.sort_values('probs', axis=0,
                        ascending=True, inplace=True,
                        kind='mergesort')
    print to_plot

    fig, ax = plt.subplots(figsize=(7,3))
    plt.title('Model Prediction: '+probs[0][0])
    plt.ylabel('Species Group')
    plt.xlabel('Prediction Strength')
    ax.set_yticklabels(to_plot['groups'], rotation=50, ha='right')

    plt.barh(range(0,5), to_plot['probs'], color='#6982A0', alpha=0.8)

    if save_as:
        plt.savefig('data/presentation/{}.png'.format(save_as), bbox_inches='tight')

    plt.show()
    return to_plot


# plot confusion matrix or percentage matrix
def plot_matrix(matrix, y_test, y_pred, save_as = None):

    true_labels = np.unique(y_test)
    pred_labels = np.unique(y_pred)
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion matrix", fontsize=16)
    cbar = plt.colorbar(fraction=0.046, pad=0.04)
    cbar.set_label('Percent True', rotation=270, labelpad=30, fontsize=12)
    xtick_marks = np.arange(len(true_labels)+1)
    ytick_marks = np.arange(len(pred_labels)+1)
    plt.xticks(xtick_marks, true_labels, rotation=90)
    plt.yticks(ytick_marks,pred_labels)
    plt.tight_layout()
    plt.ylabel('True label', fontsize=14)
    plt.xlabel('Predicted label', fontsize=14)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 10
    fig_size[1] = 10
    plt.rcParams["figure.figsize"] = fig_size
    if save_as:
        plt.savefig('data/presentation/{}.png'.format(save_as), bbox_inches='tight')
    plt.show()
