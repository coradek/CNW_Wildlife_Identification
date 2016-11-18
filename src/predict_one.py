import cPickle as pickle
import src.feature_extractor as fe


# Predict animal
def predict(image):

    X = fe.extract_features([image])

    with open('data/current_model', 'rb') as fh:
        model = pickle.load(fh)

    prediction = model.predict(X)

    return prediction
