import cPickle as pickle
import src.feature_extractor as fe


# Predict animal
def predict(image, model = 'current_model'):

    X = fe.extract_features([image])
    model_path = 'data/'+model+'.pkl'

    with open(model_path, 'rb') as fh:
        model = pickle.load(fh)

    prediction = model.predict(X)

    try:
        probs = model.predict_proba(X)
        print 'prediction prepared'
        return prediction, probs
    # if model does not have predict_proba - pass
    except AttributeError:
        pass

    print 'prediction prepared'
    return prediction
