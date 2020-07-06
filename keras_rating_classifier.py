import csv
import numpy as np
import random
import os
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD, Adam, Adamax, Adagrad, Nadam
from keras.constraints import maxnorm
import pickle
import wandb
from wandb.keras import WandbCallback
utils = __import__('227_utils')


LEARNING_RATE = 0.0005
BATCH_SIZE = 50
EPOCHS = 250
OPTIMIZER = "adamax"  # sdg, adam, adamax, adagrad, nadam
ACTIVATION_FUNC = "tanh"  # tanh, sigmoid
DROPOUT_RATE = 0.4
EMBEDDING_TYPE = "embeddings"  # embeddings, embeddings-unspeech (embeddings dir name)
TRAINING_DATA = "anonymized"  # anonymized, split-10, ... (subdir name in wavs dir)
AUGMENTATION_BY_INVERSION = False  # Double the amount of data by inverting the order of each rating?
TEST_SET_MIN_SIZE = 100  # Minimum size of each test set. This will automatically be increased if augmentation is on.

wandb.init(
    config={"learning_rate": LEARNING_RATE,
            "batch size": BATCH_SIZE,
            "epochs": EPOCHS,
            "optimizer": OPTIMIZER,
            "activation_func": ACTIVATION_FUNC,
            "dropout_rate": DROPOUT_RATE,
            "embedding_type": EMBEDDING_TYPE,
            "training_data": TRAINING_DATA,
            "augmentation_by_inversion": AUGMENTATION_BY_INVERSION,
            "test_set_min_size": TEST_SET_MIN_SIZE},
    project=["Speech-Quality-Classifier-ratings"]
)


embeddings = []
for root, dirs, files in os.walk(os.path.join(EMBEDDING_TYPE, TRAINING_DATA)):
    for f in files:
        embeddings.append(pickle.load(open(os.path.join(root, f), 'rb')))


def to_embedding_diff_data_and_labels(dataset):
    labels = np.array(dataset)[:, 2:3]
    embeddings_a = np.array(list(map(lambda x: embeddings[x[0]], np.array(dataset)[:, 0:1])))
    embeddings_b = np.array(list(map(lambda x: embeddings[x[0]], np.array(dataset)[:, 1:2])))
    return embeddings_a - embeddings_b, labels


def accuracy_based_on_ranking(dataset):
    predicted_labels = list(map(lambda r: utils.predict_based_on_ranking(r[:2], external_speakers), dataset))
    correct_counter = 0
    for i in range(len(dataset)):
        if predicted_labels[i] == dataset[i][2]:
            correct_counter += 1
    return correct_counter / len(dataset)


with open('ratings.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

data = list(map(lambda r: list(map(lambda i: int(i), r)), data))

if AUGMENTATION_BY_INVERSION:
    print("Doubling dataset size by inverting order of each rating ...")
    data_order_inverted = list(map(lambda r: [r[1], r[0], int(not r[2])], data.copy()))
    data = data + data_order_inverted
    TEST_SET_MIN_SIZE *= 2

random.shuffle(data)
print(str(len(data)) + " pairwise comparisons in total.")
test_external, external_speakers = [], []
while len(test_external) < TEST_SET_MIN_SIZE:
    external_speakers += [random.randint(0, 226) for i in range(1)]
    test_external += [x for x in data if (utils.includes_external_speakers(x, external_speakers))]
data = [x for x in data if x not in test_external]
print("test_external:   " + str(len(test_external)))
test_naive = data[:TEST_SET_MIN_SIZE]
print("test_naive:      " + str(len(test_naive)))
test_50 = [x for x in data if (utils.has_ranking_distance(x, 0.5))][:TEST_SET_MIN_SIZE]
print("test_50:         " + str(len(test_50)))
random.shuffle(data)
test_25 = [x for x in data if (utils.has_ranking_distance(x, 0.25))][:TEST_SET_MIN_SIZE]
print("test_25:         " + str(len(test_25)))
train = [x for x in data if x not in (test_naive + test_50 + test_25)]
print("train:           " + str(len(train)))
print("Ratings included in test sets may overlap.")

test_sets = [test_naive, test_50, test_25, test_external]
test_set_names = ["test_naive", "test_50", "test_25", "test_external"]

print("\nPrediction accuracies based only on ranking:")
for dataset, name in zip([train] + test_sets, ["train"] + test_set_names):
    score = accuracy_based_on_ranking(dataset)
    print(f'{name + ":": <15} {score:.2f}')
    wandb.log({name + "_by_ranking": score})


train_data, train_labels = to_embedding_diff_data_and_labels(train)


model = Sequential()
model.add(Dense(256, input_dim=256))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(256, kernel_constraint=maxnorm(3)))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(256, kernel_constraint=maxnorm(3)))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(256, kernel_constraint=maxnorm(3)))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dropout(DROPOUT_RATE))
model.add(Dense(128, kernel_constraint=maxnorm(3)))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dense(64, kernel_constraint=maxnorm(3)))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dense(32))
model.add(Activation(ACTIVATION_FUNC))
model.add(Dense(1))
model.add(Activation(ACTIVATION_FUNC))

switcher = {
    "sgd": SGD(learning_rate=LEARNING_RATE),
    "adam": Adam(learning_rate=LEARNING_RATE),
    "adamax": Adamax(learning_rate=LEARNING_RATE),
    "adagrad": Adagrad(learning_rate=LEARNING_RATE),
    "nadam": Nadam(learning_rate=LEARNING_RATE)
}

model.compile(loss='binary_crossentropy', optimizer=switcher.get(OPTIMIZER), metrics=["binary_accuracy"])

model.fit(train_data, train_labels, batch_size=BATCH_SIZE, nb_epoch=EPOCHS, callbacks=[WandbCallback()])

print("\nPrediction accuracies based on embeddings:")
for test_set, name in zip(test_sets, test_set_names):
    test_data, test_labels = to_embedding_diff_data_and_labels(test_set)
    scores = model.evaluate(test_data, test_labels, verbose=0)
    print(f'{name+":": <15} {scores[1]:.2f}')
    wandb.log({name: scores[1]})
