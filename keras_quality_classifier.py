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

LEARNING_RATE = 0.0005
BATCH_SIZE = 50
EPOCHS = 250
OPTIMIZER = "adamax"  # sdg, adam, adamax, adagrad, nadam
ACTIVATION_FUNC = "tanh"  # tanh, sigmoid
DROPOUT_RATE = 0.4
EMBEDDING_TYPE = "embeddings"  # embeddings, embeddings-unspeech (embeddings dir name)
TRAINING_DATA = "split-10"  # anonymized, split-10, ... (subdir name in wavs dir)

wandb.init(
    config={"learning_rate": LEARNING_RATE,
            "batch size": BATCH_SIZE,
            "epochs": EPOCHS,
            "optimizer": OPTIMIZER,
            "activation_func": ACTIVATION_FUNC,
            "dropout_rate": DROPOUT_RATE,
            "embedding_type": EMBEDDING_TYPE,
            "training_data": TRAINING_DATA},
    project=["Speech-Quality-Classifier-quality"]
)


