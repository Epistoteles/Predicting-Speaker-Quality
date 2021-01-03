from matplotlib import pyplot as plt
from statistics import mean
import pickle
import os
import numpy as np
import seaborn as sns
import math


def plot_predictions_as_histogram(predictions, truths, feature_type, dataset, timeseries, knn):
    """
    Takes in list of predictions and plots them as a histogram. If valid truths
    are supplied as well, they are added as second histogram for comparison.
    """
    plt.figure(figsize=(12, 7))
    sns.set_style("darkgrid")
    bins = np.linspace(0, 1, 50)  # 50 bins from 0 to 1
    plt.xlim(0, 1)
    truths = [item for sublist in truths for item in sublist]
    predictions = [item for sublist in predictions for item in sublist]
    plt.hist(truths, bins=bins, alpha=0.5, label='Ground truth')
    plt.axvline(x=mean(truths), color='dodgerblue', linestyle='--')
    plt.text(mean(truths) + 0.01, 0.93, f'Ground truth mean: {mean(truths):.3f}',
             transform=plt.gca().transAxes, color='dodgerblue',
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.hist(predictions, bins=bins, alpha=0.5, label='Predictions')
    plt.axvline(x=mean(predictions), color='darkorange', linestyle='--')
    plt.text(mean(predictions) + 0.01, 0.87,
             f'Prediction mean: {mean(predictions):.3f}',
             transform=plt.gca().transAxes, color='darkorange',
             bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.title(f'Prediction quality histogram using {feature_type}')
    plt.xlabel('predicted quality')
    plt.ylabel('count')
    plt.legend(loc='upper left')
    plt.savefig(f"../graphics/plots/prediction-histogram-{feature_type}{'-lstm' if timeseries else '-knn' if knn else ''}.png", dpi=300)
    plt.close()


def plot_predictions_as_density(predictions, feature_type, timeseries, knn):
    """
    Takes in list of predictions and plots them as a density plot per fold.
    """
    plt.figure(figsize=(12, 7))
    sns.set_style("darkgrid")
    plt.xlim(0, 1)
    if len(predictions) == 10:
        for i in range(10):
            sns.distplot(predictions[i], hist=False, kde=True,
                         kde_kws={'linewidth': 3},
                         label=f"Predictions of fold {i+1}/10")
    plt.title(f'Prediction quality density using {feature_type}')
    plt.xlabel('predicted quality')
    plt.ylabel('count')
    plt.legend(loc='upper left')
    plt.savefig(f"../graphics/plots/prediction-density-{feature_type}{'-lstm' if timeseries else '-knn' if knn else ''}.png", dpi=300)
    plt.close()


def plot_predictions_as_scatterplot(predictions, truths, feature_type, timeseries, knn):
    """
    Takes in list of predictions and truths and plots them as scatterplot.
    """
    plt.figure(figsize=(10, 9))
    sns.set_style("darkgrid")
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    if len(predictions) == 10:
        for i in range(10):
            sns.scatterplot(truths[i], predictions[i], label=f"val set of fold {i + 1}/10")
    plt.title(f'Predictions using {feature_type}')
    plt.xlabel('true quality')
    plt.ylabel('predicted quality')
    plt.legend(loc='upper left')
    plt.savefig(f"../graphics/plots/prediction-scatter-{feature_type}{'-lstm' if timeseries else '-knn' if knn else ''}.png", dpi=300)
    plt.close()


def plot_desired_scatterplot(truths, feature_type):
    """
    Takes in list of predictions and truths and plots them as scatterplot.
    """
    plt.figure(figsize=(10, 9))
    sns.set_style("darkgrid")
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    if len(truths) == 10:
        for i in range(10):
            noisy_truth = list(map(lambda x: min(1, max(0, x * 0.8 + 0.1 +
                            np.random.normal(0, 0.1) * (math.sin(x * math.pi) * 0.5 + 0.5))), truths[i]))
            sns.scatterplot(truths[i], noisy_truth, label=f"val set of fold {i + 1}/10")
    plt.title(f'Desired predictions for all featured')
    plt.xlabel('true quality')
    plt.ylabel('true quality +/- normally distributed noise')
    plt.legend(loc='upper left')
    plt.savefig(f'../graphics/plots/prediction-scatter-desired.png', dpi=300)
    plt.close()


def plot_predictions(feature_type, predictions=None, timeseries=False, knn=False, dataset='split-10'):
    if predictions is None:
        predictions = os.listdir('../predictions/')
        predictions = sorted([m for m in predictions if m.startswith(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else '0'}")],
            key=lambda x: float(x.split('-')[3 if timeseries or knn else 2]))
        predictions = predictions[0]
    (predictions, truths) = pickle.load(open(f'../predictions/{predictions}', 'rb'))
    # for some reason, predictions for timeseries are series
    # I didn't have the time to fix this, so I take the mean of each predicted series
    if timeseries:
        new_predictions = []
        for i in range(10):
            compressed_predictions = []
            factor = int(len(predictions[i]) / len(truths[i]))
            for j in range(len(truths[i])):
                compressed_predictions += [mean(predictions[i][j*factor:(j+1)*factor])]
            new_predictions += [compressed_predictions]
        predictions = new_predictions
    plot_predictions_as_histogram(predictions, truths, feature_type, dataset, timeseries, knn)
    plot_predictions_as_density(predictions, feature_type, timeseries, knn)
    plot_predictions_as_scatterplot(predictions, truths, feature_type, timeseries, knn)
    plot_desired_scatterplot(truths, feature_type)


plot_predictions('embeddings-ge2e')
plot_predictions('embeddings-trill')

plot_predictions('feature-streams', timeseries=True)
plot_predictions('embeddings-ge2e', timeseries=True)
plot_predictions('embeddings-trill', timeseries=True)

plot_predictions('embeddings-ge2e', knn=True)
plot_predictions('embeddings-trill', knn=True)
