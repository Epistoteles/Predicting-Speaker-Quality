import os
import pickle
from cross_validation_generator import load_feature_stream, load_samples
import numpy as np
from tensorflow.keras.models import load_model


def load_features(feature_type, timeseries=False, dataset='demo'):
    """
    Loads features of all wavs in the demo directory into a list and
    returns it together with filenames and ground truths (if existent).
    """
    if dataset is 'split-10':
        samples = load_samples(feature_type, dataset, timeseries)
        features = [s.feature for s in samples]
        truths = [s.Speaker.quality for s in samples]
        filenames = [f"{'/'.join(s.speaker, s.article, s.section)}.wav" for s in samples]
        return features, filenames, truths
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
    return features, filenames, len(features) * [-1]


def predict_speakers(feature_type, model=None, timeseries=False, dataset='demo'):
    """
    Print out predictions for wavs in demo directory using specific feature type
    with the best model for that feature type.
    """
    features, filenames, truths = load_features(feature_type, timeseries, dataset)
    print(features[0])
    if model is None:
        models = os.listdir('models/')
        models = sorted([m for m in models if m.startswith(f"{feature_type}-{'LSTM' if timeseries else '0'}")],
                        key=lambda x: float(x.split('-')[2]))
        model = models[0]
    print(f"Loading model models/{model} ...")
    model = load_model(f'models/{model}')
    model.summary()
    predictions = []
    for feature, filename in zip(features, filenames):
        feature = feature.transpose()
        # print(f'Feature: {feature}')
        # print(feature.shape)
        # print(f'Filename: {filename}')
        prediction = model(np.array([feature, ]), training=False)
        print(f'Prediction for {filename}: {prediction[0][0]:5f} out of 1')
        predictions += prediction.numpy().tolist()[0]
    print(predictions)
    print(len(predictions))


predict_speakers('embeddings-ge2e', dataset='split-10')
