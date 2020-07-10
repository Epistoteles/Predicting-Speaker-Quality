import csv
import numpy as np
import random
import os
import pickle
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD, Adam, Adamax, Adagrad, Nadam
from keras.constraints import maxnorm
import wandb
from wandb.keras import WandbCallback
from sklearn.utils import shuffle
utils = __import__('227_utils')


LEARNING_RATE = 0.0000005
BATCH_SIZE = 10
EPOCHS = 100
OPTIMIZER = "adamax"  # sdg, adam, adamax, adagrad, nadam
ACTIVATION_FUNC = "tanh"  # tanh, sigmoid
DROPOUT_RATE = 0.5
VAL_SPLIT = 0.1
LOSS = "mean_squared_error"
EMBEDDING_TYPE = "embeddings"  # embeddings, embeddings-unspeech (embeddings dir name)
TRAINING_DATA = "split-10"  # split-10, ... (subdir name in wavs dir)

wandb.init(
    config={"learning_rate": LEARNING_RATE,
            "batch size": BATCH_SIZE,
            "epochs": EPOCHS,
            "optimizer": OPTIMIZER,
            "activation_func": ACTIVATION_FUNC,
            "dropout_rate": DROPOUT_RATE,
            "val_split": VAL_SPLIT,
            "loss": LOSS,
            "embedding_type": EMBEDDING_TYPE,
            "training_data": TRAINING_DATA},
    project="SQE-quality"
)

speaker_to_quality_dict = pickle.load(open("speaker_to_quality_dict.pickle", "rb"))

# for speaker, quality in speaker_to_quality_dict.items():
#     if quality < 0:
#         print(speaker)

embeddings = []
speakers = []
articles = []
qualities = []

for root, dirs, files in os.walk(os.path.join(EMBEDDING_TYPE, TRAINING_DATA)):
    root_list = root.split("/")
    if len(root_list) == 4:
        _, _, speaker, article = root_list
        speaker_quality = speaker_to_quality_dict[speaker]
        if speaker in speaker_to_quality_dict and speaker_quality >= 0:
            for f in files:
                if f.endswith(".p"):  # TODO replace with .pickle
                    embedding = pickle.load(open(os.path.join(root, f), "rb"))
                    embeddings.append(embedding)
                    speakers.append(speaker)
                    articles.append(article)
                    qualities.append(speaker_quality)

print("done generating lists")
print(len(qualities))

external_indices = set()

while len(external_indices) < 0.1 * len(qualities):
    external_speaker = random.sample(set(speakers), 1)[0]
    for i, s in enumerate(speakers):
        if s == external_speaker:
            external_indices.add(i)

print("# external_indices: " + str(len(external_indices)))

x_train = []
y_train = []

x_test = []
y_test = []

for i, (x, y) in enumerate(zip(embeddings, qualities)):
    if i in external_indices:
        x_test.append(x)
        y_test.append(y)
    else:
        x_train.append(x)
        y_train.append(y)

print(len(x_train))
print(len(y_train))
print(len(x_test))
print(len(y_test))

x_train = np.array(x_train)
y_train = np.array(y_train)

x_test = np.array(x_test)
y_test = np.array(y_test)

x_train, y_train = shuffle(x_train, y_train)


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

model.compile(loss=LOSS, optimizer=switcher.get(OPTIMIZER), metrics=[LOSS])

model.fit(
    x_train,
    y_train,
    # validation_split=VAL_SPLIT,
    batch_size=BATCH_SIZE,
    nb_epoch=EPOCHS,
    validation_data=(x_test, y_test),
    callbacks=[WandbCallback()]
)

model.evaluate(x_test, y_test)
