import pickle
import os
from statistics import mean, stdev


def calculate_speaker_spread(feature_type, predictions=None, timeseries=False, knn=False, rf=False, dataset='split-10'):
    if predictions is None:
        predictions = os.listdir('predictions/')
        predictions = sorted([m for m in predictions if m.startswith(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else 'RF' if rf else '0'}")],
            key=lambda x: float(x.split('-')[3 if timeseries or knn or rf else 2]))
        predictions = predictions[0]
    predictions, truths = pickle.load(open(f'predictions/{predictions}', 'rb'))
    if timeseries:
        new_predictions = []
        for i in range(10):
            compressed_predictions = []
            factor = int(len(predictions[i]) / len(truths[i]))
            for j in range(len(truths[i])):
                compressed_predictions += [mean(predictions[i][j*factor:(j+1)*factor])]
            new_predictions += [compressed_predictions]
        predictions = new_predictions
    predictions = [item for sublist in predictions for item in sublist]
    truths = [item for sublist in truths for item in sublist]
    grouped_speakers = {}
    for pair in zip(predictions, truths):
        score, truth = pair
        if truth not in grouped_speakers:
            grouped_speakers[truth] = []
        grouped_speakers[truth] = grouped_speakers[truth] + [score]
    # print(grouped_speakers.values()[0])
    avg_spans = []
    avg_sds = []
    for scores in grouped_speakers.values():
        avg_span = abs(max(scores)-min(scores))
        avg_sd = stdev(scores)
        avg_spans += [avg_span]
        avg_sds += [avg_sd]
    print(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else 'RF' if rf else '0'}")
    print(f"Average intra-speaker score span: {mean(avg_spans)}")
    print(f"Average intra-speaker score sd: {mean(avg_sds)}")
    print("----")


def calculate_sd_proportions(feature_type, predictions=None, timeseries=False, knn=False, rf=False, dataset='split-10'):
    if predictions is None:
        predictions = os.listdir('predictions/')
        predictions = sorted([m for m in predictions if m.startswith(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else 'RF' if rf else '0'}")],
            key=lambda x: float(x.split('-')[3 if timeseries or knn or rf else 2]))
        predictions = predictions[0]
    predictions, truths = pickle.load(open(f'predictions/{predictions}', 'rb'))
    if timeseries:
        new_predictions = []
        for i in range(10):
            compressed_predictions = []
            factor = int(len(predictions[i]) / len(truths[i]))
            for j in range(len(truths[i])):
                compressed_predictions += [mean(predictions[i][j*factor:(j+1)*factor])]
            new_predictions += [compressed_predictions]
        predictions = new_predictions
    proportions = []
    for fold in zip(predictions, truths):
        grouped_speakers = {}
        for score, truth in zip(fold[0], fold[1]):
            if truth not in grouped_speakers:
                grouped_speakers[truth] = []
            grouped_speakers[truth] = grouped_speakers[truth] + [score]
        avg_sds = []
        for scores in grouped_speakers.values():
            avg_sd = stdev(scores)
            avg_sds += [avg_sd]
        proportion = mean(avg_sds) / stdev(fold[0])
        proportions += [proportion]

    print(f"{feature_type}-{'LSTM' if timeseries else 'KNN' if knn else 'RF' if rf else '0'}")
    print(f"Average sd-sd proportions: {mean(proportions)}")
    print("----")
    global temp
    temp += [mean(proportions)]


# calculate_speaker_spread('feature-streams', timeseries=True)
# calculate_speaker_spread('feature-streams')
# calculate_speaker_spread('feature-streams', knn=True)
# calculate_speaker_spread('feature-streams', rf=True)
#
# calculate_speaker_spread('embeddings-ge2e')
# calculate_speaker_spread('embeddings-ge2e', knn=True)
# calculate_speaker_spread('embeddings-ge2e', rf=True)
#
# calculate_speaker_spread('embeddings-trill', timeseries=True)
# calculate_speaker_spread('embeddings-trill')
# calculate_speaker_spread('embeddings-trill', knn=True)
# calculate_speaker_spread('embeddings-trill', rf=True)

temp = []

calculate_sd_proportions('feature-streams', timeseries=True)
calculate_sd_proportions('feature-streams')
calculate_sd_proportions('feature-streams', knn=True)
calculate_sd_proportions('feature-streams', rf=True)

calculate_sd_proportions('embeddings-ge2e')
calculate_sd_proportions('embeddings-ge2e', knn=True)
calculate_sd_proportions('embeddings-ge2e', rf=True)

calculate_sd_proportions('embeddings-trill', timeseries=True)
calculate_sd_proportions('embeddings-trill')
calculate_sd_proportions('embeddings-trill', knn=True)
calculate_sd_proportions('embeddings-trill', rf=True)

print(temp)