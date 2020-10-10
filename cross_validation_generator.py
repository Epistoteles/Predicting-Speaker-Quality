import os
import pickle
import numpy as np
from statistics import mean, stdev
np.set_printoptions(precision=3)


def get_folds(embedding_type, dataset, folds=10, seed=None):
    """
    Takes in the embedding type to use as well as the dataset to use
    and returns folds times a train set and val set with data and labels
    in the order x_train, y_train, x_val, y_val.
    """
    # set seed if given
    if seed is not None:
        np.random.seed(seed)

    # get qualities for each speaker
    speaker_to_quality_dict = pickle.load(open("speaker_to_quality_dict.pickle", "rb"))

    embeddings = []
    speakers = []
    articles = []
    qualities = []

    # fill in embeddings, speakers, spoken articles and speaker qualities into lists
    for root, dirs, files in os.walk(os.path.join(embedding_type, dataset)):
        root_list = root.split("/")
        if len(root_list) == 4:
            _, _, speaker, article = root_list
            quality = speaker_to_quality_dict[speaker]
            if speaker in speaker_to_quality_dict and quality >= 0:
                for f in files:
                    if f.endswith(".pickle"):
                        embedding = pickle.load(open(os.path.join(root, f), "rb"))
                        embeddings.append(embedding)
                        speakers.append(speaker)
                        articles.append(article)
                        qualities.append(quality)

    # sort the used/appearing speakers by quality
    speakers_ordered_by_quality = sorted(speaker_to_quality_dict, key=speaker_to_quality_dict.get)
    print(f'number of speakers: {len(speakers_ordered_by_quality)}')
    speakers_ordered_by_quality = list(x for x in speakers_ordered_by_quality if x in set(speakers))
    print(f'number of speakers with quality rating and audio: {len(speakers_ordered_by_quality)}')
    print(speakers_ordered_by_quality)

    # create 10 quantiles for the speakers by quality
    speaker_bins = np.array_split(speakers_ordered_by_quality, 20)

    # shuffle the speakers in each quantile
    for i in range(len(speaker_bins)):
        np.random.shuffle(speaker_bins[i])

    # create k empty folds
    k_folds = [[] for _ in range(folds)]

    # fill the folds iteratively with speakers from each bin
    while max(list(map(lambda x: len(x), speaker_bins))) != 0:
        for i in range(folds):
            for j in range(len(speaker_bins)):
                if len(speaker_bins[j]):
                    # this simulates list.pop()
                    random_index = np.random.randint(0, len(speaker_bins[j]))
                    k_folds[i].append(speaker_bins[j][random_index])
                    speaker_bins[j] = np.delete(speaker_bins[j], random_index)
    print(k_folds)

    # print stats about the speakers in each fold
    print('Speakers in each fold:')
    print(np.array(list(map(lambda x: len(x), k_folds))))
    print('Speaker quality mean in each fold:')
    print(np.array(list(map(lambda fold: mean(list(map(lambda x: speaker_to_quality_dict[x], fold))), k_folds))))
    print(k_folds)
    print('Speaker quality std dev in each fold:')
    print(np.array(list(map(lambda fold: stdev(list(map(lambda x: speaker_to_quality_dict[x], fold))), k_folds))))

    # build x_train, y_train, x_val and y_val based on the speakers in each fold
    while folds > 0:
        folds -= 1
        train = [item for sublist in k_folds[:folds] + k_folds[folds + 1:] for item in sublist]
        val = k_folds[folds]
        x_train = [embeddings[index] for index, element in enumerate(speakers) if element in train]
        y_train = [qualities[index] for index, element in enumerate(speakers) if element in train]
        x_val = [embeddings[index] for index, element in enumerate(speakers) if element in val]
        y_val = [qualities[index] for index, element in enumerate(speakers) if element in val]

        # yield new sets for each next(generator) call
        yield x_train, y_train, x_val, y_val


def generator_test(seed):
    """Tests the function above"""
    # collect some stats per fold
    size_train = []
    size_val = []
    amount_speakers_train = []
    amount_speakers_val = []
    mean_embeddings_per_speaker_train = []
    mean_embeddings_per_speaker_val = []
    stdev_embeddings_per_speaker_train = []
    stdev_embeddings_per_speaker_val = []
    quality_mean_per_speaker_train = []
    quality_mean_per_speaker_val = []
    quality_mean_per_embedding_train = []
    quality_mean_per_embedding_val = []
    quality_stdev_per_speaker_train = []
    quality_stdev_per_speaker_val = []
    quality_stdev_per_embedding_train = []
    quality_stdev_per_embedding_val = []

    # create generator and get all folds produced
    generator = get_folds('embeddings-ge2e', 'split-10', 10, seed=seed)
    for i in range(10):
        n = next(generator)
        # n[0] = train embeddings
        # n[1] = train qualities
        # n[2] = val embeddings
        # n[3] = val qualities

        # fill stats
        size_train += [len(n[0])]
        size_val += [len(n[2])]
        amount_speakers_train += [len(set(n[1]))]
        amount_speakers_val += [len(set(n[3]))]
        mean_embeddings_per_speaker_train += [mean(map(lambda x: n[1].count(x), set(n[1])))]
        mean_embeddings_per_speaker_val += [mean(map(lambda x: n[3].count(x), set(n[3])))]
        stdev_embeddings_per_speaker_train += [stdev(map(lambda x: n[1].count(x), set(n[1])))]
        stdev_embeddings_per_speaker_val += [stdev(map(lambda x: n[3].count(x), set(n[3])))]
        quality_mean_per_speaker_train += [mean(set(n[1]))]
        quality_mean_per_speaker_val += [mean(set(n[3]))]
        quality_mean_per_embedding_train += [mean(n[1])]
        quality_mean_per_embedding_val += [mean(n[3])]
        quality_stdev_per_speaker_train += [stdev(set(n[1]))]
        quality_stdev_per_speaker_val += [stdev(set(n[3]))]
        quality_stdev_per_embedding_train += [stdev(n[1])]
        quality_stdev_per_embedding_val += [stdev(n[3])]

    size_val_stdev = stdev(size_val)

    print('-------------------------')
    print(f'Results for seed {seed}:')
    print('size')
    print(size_train)
    print(size_val)
    print('amount of speakers')
    print(amount_speakers_train)
    print(amount_speakers_val)
    print('mean amount of embeddings per speaker')
    print(np.array(mean_embeddings_per_speaker_train))
    print(np.array(mean_embeddings_per_speaker_val))
    print('stdev amount of embeddings per speaker')
    print(np.array(stdev_embeddings_per_speaker_train))
    print(np.array(stdev_embeddings_per_speaker_val))
    print('mean quality per speaker')
    print(np.array(quality_mean_per_speaker_train))
    print(np.array(quality_mean_per_speaker_val))
    print('stdev quality per speaker')
    print(np.array(quality_stdev_per_speaker_train))
    print(np.array(quality_stdev_per_speaker_val))
    print('mean quality per embedding')
    print(np.array(quality_mean_per_embedding_train))
    print(np.array(quality_mean_per_embedding_val))
    print('stdev quality per embedding')
    print(np.array(quality_stdev_per_embedding_train))
    print(np.array(quality_stdev_per_embedding_val))
    print(f'Standard deviation of val sizes: {size_val_stdev}')
    print('++++++++++++++++++')

    return size_val_stdev

print(generator_test(692))

best_seed = 0
lowest_stdev = 100000

for i in range(1000):
    curr_stdev = generator_test(i)
    if curr_stdev < lowest_stdev:
        lowest_stdev = curr_stdev
        best_seed = i
    print(f'currently best seed: {best_seed}')
    print(f'currently lowest stdev: {lowest_stdev}')
