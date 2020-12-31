import os
import pickle
from cross_validation_generator import load_feature_stream, load_samples
import numpy as np
from tensorflow.keras.models import load_model
from matplotlib import pyplot as plt
from statistics import mean


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
    plot_predictions_as_histogram(predictions, truths, feature_type, dataset)


def plot_predictions_as_histogram(predictions, truths, feature_type, dataset):
    """
    Takes in list of predictions and plots them as a histogram. If valid truths
    are supplied as well, they are added as second histogram for comparison.
    """
    bins = np.linspace(0, 1, 50)  # 50 bins from 0 to 1
    plt.xlim(0, 1)
    plt.hist(predictions, bins=bins, alpha=0.5, label='Predictions')
    if truths[0] >= 0:
        plt.hist(truths, bins=bins, alpha=0.5, label='Ground truth')
        plt.axvline(x=mean(truths), color='darkorange', linestyle='--')
        plt.text(mean(truths) + 0.01, 0.93, f'Ground truth mean: {mean(truths):.3f}',
                 transform=plt.gca().transAxes, color='darkorange',
                 bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.axvline(x=mean(predictions), color='dodgerblue', linestyle='--')
    plt.text(mean(predictions) + 0.01, 0.87, f'Prediction mean: {mean(predictions):.3f}',
             transform=plt.gca().transAxes, color='dodgerblue',
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.title(f'Predictions using {feature_type}')
    plt.xlabel('Predictions in 50 bins')
    plt.ylabel('count')
    plt.legend(loc='upper left')
    if dataset == 'split-10':
        plt.savefig(f'graphics/plots/prediction-vs-truth-{feature_type}.png')
    plt.show()


predict_speakers('embeddings-ge2e', dataset='split-10')
