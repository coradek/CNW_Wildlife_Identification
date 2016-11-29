import os
import re
import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile
import numpy as np
import pandas as pd
import cPickle as pickle


def create_graph():
    model_dir = 'imagenet'
    with gfile.FastGFile(os.path.join(
        model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


#TODO: separate graph creation and tf.Session
def extract_features(list_images):
    '''take list of image file paths
    return pandas series of features
    '''

    nb_features = 2048
    features = np.empty((len(list_images),nb_features))

    create_graph()

    with tf.Session() as sess:

        next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        for ind, image in enumerate(list_images):

            if not gfile.Exists(image):
                tf.logging.fatal('File does not exist %s', image)

            image_data = gfile.FastGFile(image, 'rb').read()

            predictions = sess.run(next_to_last_tensor,
                                {'DecodeJpeg/contents:0': image_data})
            features[ind,:] = np.squeeze(predictions)

    return features


# Predict animal
def predict(image, model = 'current_model'):

    X = extract_features([image])

    with open(model, 'rb') as fh:
        model = pickle.load(fh)

    prediction = model.predict(X)

    try:
        probs = model.predict_proba(X)
        print 'prediction prepared'
        return prediction, probs
    except AttributeError:
        pass

    print 'prediction prepared'
    return prediction


def get_probs():
    # get prediction/ prob array
    # return array to webapp
    pass

def plot_probs():
    #plot prob array
    # return plot (png?) to webapp
    pass

#TODO: rework separate into two steps (above)
def plot_probs(probs, save_as = None):

    # create ordered DataFrame of categories and probabilities
    groups = ['Canine', 'Feline', 'Other', 'Small', 'Ungulate']
    to_plot = pd.DataFrame(groups, columns = ['groups'])
    to_plot['pred_strength'] = probs[1][0]
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

if __name__ == '__main__':
    main()
