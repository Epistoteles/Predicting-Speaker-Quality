import os
import pickle
from cross_validation_generator import load_feature_stream
import numpy as np
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation, Dropout, Bidirectional, LSTM
from tensorflow.keras.optimizers import SGD, Adam, Adamax, Adagrad, Nadam
from tensorflow.keras.constraints import MaxNorm
from tensorflow.keras.callbacks import EarlyStopping, History
from keras_self_attention import SeqSelfAttention
from sklearn.utils import shuffle
from statistics import mean
from human_id import generate_id


def load_demo_features(feature_type, timeseries=False, dataset='demo'):
    """
    Loads features of all wavs in the demo directory into a list
    and returns it
    """
    features = []
    filenames = []
    for root, _, files in os.walk(os.path.join('wavs', dataset)):
        for f in files:
            if f.endswith('.wav'):
                section = f.split('.wav')[0]
                if feature_type == 'embeddings-ge2e':
                    feature = (pickle.load(
                        open(os.path.join(root.replace('wavs/', f'{feature_type}/'), f'{section}.pickle'),
                             'rb')))
                    features.append(feature)
                elif feature_type == 'embeddings-trill':
                    feature = pickle.load(
                        open(os.path.join(root.replace('wavs/', f'{feature_type}/'), f'{section}.pickle'),
                             'rb'))
                    features.append(feature if timeseries else np.mean(feature, axis=0))
                elif feature_type == 'feature-streams':
                    feat_stream = load_feature_stream(dataset,
                                                      os.path.join(root.replace('wavs/', f'{feature_type}/'),
                                                                   f'{section}'))
                    features.append(feat_stream if timeseries else np.mean(feat_stream, axis=0))
            filenames.append(f)
    return features, filenames


def predict_demo_speakers(model, feature_type, timeseries=False, dataset='demo'):
    """
    Print out predictions for wavs in demo directory using specific feature type
    the best model for that feature type.
    """
    features, filenames = load_demo_features(feature_type, timeseries, dataset)
    model = load_model(model)
    for feature, filename in zip(features, filenames):
        prediction = model(feature, training=False)
        print(f'Prediction for {filename}: {prediction} out of 1')


predict_demo_speakers('models/model', 'embeddings-ge2e')