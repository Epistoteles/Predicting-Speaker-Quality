from matplotlib import pyplot as plt
from statistics import mean
import pickle
import os
import numpy as np
import seaborn as sns
import math
from numpy.polynomial.polynomial import polyfit
from scipy.stats import pearsonr


sns_style = "darkgrid"

def plot_predictions_as_histogram(predictions, truths, feature_type, dataset, timeseries, knn, rf):
    """
    Takes in list of predictions and plots them as a histogram. If valid truths
    are supplied as well, they are added as second histogram for comparison.
    """
    plt.figure(figsize=(12, 7))
    sns.set_style(sns_style)
    bins = np.linspace(0, 1, 50)  # 50 bins from 0 to 1
    plt.xlim(0, 1)
    plt.ylim(0, 700)
    truths = [item for sublist in truths for item in sublist]
    predictions = [item for sublist in predictions for item in sublist]
    plt.hist(truths, bins=bins, alpha=0.5, label='Ground truth')
    plt.axvline(x=mean(truths), color='dodgerblue', linestyle='--')
    # plt.text(mean(truths) + 0.01, 0.93, f'Ground truth mean: {mean(truths):.3f}',
    #         transform=plt.gca().transAxes, color='dodgerblue',
    #         bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.hist(predictions, bins=bins, alpha=0.5, label='Predictions')
    plt.axvline(x=mean(predictions), color='darkorange', linestyle='--')
    # plt.text(mean(predictions) + 0.01, 0.87,
    #         f'Prediction mean: {mean(predictions):.3f}',
    #         transform=plt.gca().transAxes, color='darkorange',
    #         bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=1))
    plt.title('')  # (f"Prediction score histogram using {feature_type}{' LSTM' if timeseries else ' kNN' if knn else ' RF' if rf else ' DNN'}")
    plt.xlabel('predicted score')
    plt.ylabel('count')
    plt.legend('')  # (loc='upper left')
    plt.savefig(f"../plots/prediction-histogram-{feature_type}{'-lstm' if timeseries else '-knn' if knn else '-rf' if rf else ''}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()


def plot_predictions_as_density(predictions, feature_type, timeseries, knn, rf):
    """
    Takes in list of predictions and plots them as a density plot per fold.
    """
    plt.figure(figsize=(12, 7))
    sns.set_style(sns_style)
    plt.xlim(0, 1)
    plt.ylim(0, 32)
    if len(predictions) == 10:
        for i in range(10):
            sns.distplot(predictions[i], hist=False, kde=True,
                         kde_kws={'linewidth': 3},
                         label=f"Predictions of fold {i+1}/10")
    # plt.title(f"Prediction score density using {feature_type}{' LSTM' if timeseries else ' kNN' if knn else ' RF' if rf else ' DNN'}")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('predicted score', fontsize=14)
    plt.ylabel('count', fontsize=14)
    plt.legend('')  # (loc='upper left')
    plt.savefig(f"../plots/prediction-density-{feature_type}{'-lstm' if timeseries else '-knn' if knn else '-rf' if rf else ''}.png", dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()


def plot_predictions_as_scatterplot(predictions, truths, feature_type, timeseries, knn, rf):
    """
    Takes in list of predictions and truths and plots them as scatterplot.
    """
    plt.figure(figsize=(10, 9))
    sns.set_style(sns_style)
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    a = []
    b = []
    if len(predictions) == 10:
        for i in range(10):
            sns.scatterplot(truths[i], predictions[i], label=f"val set of fold {i + 1}/10")
            a += truths[i]
            b += predictions[i]
    cc = np.corrcoef(a, b)
    predictions_flat = [item for sublist in predictions for item in sublist]
    truths_flat = [item for sublist in truths for item in sublist]
    b, m = polyfit(truths_flat, predictions_flat, 1)
    plt.plot(np.arange(2), b + m * np.arange(2), '-', color='dimgrey')
    r, p = pearsonr(truths_flat, predictions_flat)
    plt.text(0.5, 0.9, f"r = {r:.3f}, p {'< 0.001' if p < 0.001 else '= %.3f' % p}", fontsize=28, horizontalalignment='center', color='dimgrey')
    # plt.title(f"Predictions using {feature_type}{' LSTM' if timeseries else ' kNN' if knn else ' RF' if rf else' DNN'}")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('true score', fontsize=14)
    plt.ylabel('predicted score', fontsize=14)
    plt.legend('')  # (loc='upper left')
    plt.savefig(f"../plots/prediction-scatter-{feature_type}{'-lstm' if timeseries else '-knn' if knn else '-rf' if rf else ''}.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()


def plot_desired_scatterplot(truths, feature_type):
    """
    Takes in list of predictions and truths and plots them as scatterplot.
    """
    plt.figure(figsize=(10, 9))
    sns.set_style(sns_style)
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    if len(truths) == 10:
        for i in range(10):
            noisy_truth = list(map(lambda x: min(1, max(0, x * 0.8 + 0.1 +
                            np.random.normal(0, 0.1) * (math.sin(x * math.pi) * 0.5 + 0.5))), truths[i]))
            sns.scatterplot(truths[i], noisy_truth, label=f"val set of fold {i + 1}/10")
    plt.title(f'Desired predictions for all featured')
    plt.xlabel('true score')
    plt.ylabel('true score +/- normally distributed noise')
    plt.legend(loc='upper left')
    plt.savefig(f'../plots/prediction-scatter-desired.png', dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()


def plot_predictions(feature_type, predictions=None, timeseries=False, knn=False, rf=False, dataset='split-10'):
    if predictions is None:
        predictions = os.listdir('../predictions/')
        predictions = sorted([m for m in predictions if m.startswith(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else 'RF' if rf else '0'}")],
            key=lambda x: float(x.split('-')[3 if timeseries or knn or rf else 2]))
        predictions = predictions[0]
    (predictions, truths) = pickle.load(open(f'../predictions/{predictions}', 'rb'))
    # for some reason, predictions for timeseries are series, not just one score value
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
    plot_predictions_as_histogram(predictions, truths, feature_type, dataset, timeseries, knn, rf)
    plot_predictions_as_density(predictions, feature_type, timeseries, knn, rf)
    plot_predictions_as_scatterplot(predictions, truths, feature_type, timeseries, knn, rf)
    plot_desired_scatterplot(truths, feature_type)

plot_predictions('feature-streams', timeseries=True)
plot_predictions('feature-streams')
plot_predictions('feature-streams', knn=True)
plot_predictions('feature-streams', rf=True)

plot_predictions('embeddings-ge2e')
plot_predictions('embeddings-ge2e', knn=True)
plot_predictions('embeddings-ge2e', rf=True)

plot_predictions('embeddings-trill', timeseries=True)
plot_predictions('embeddings-trill')
plot_predictions('embeddings-trill', knn=True)
plot_predictions('embeddings-trill', rf=True)