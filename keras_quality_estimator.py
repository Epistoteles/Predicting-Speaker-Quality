import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Bidirectional, LSTM
from tensorflow.keras.optimizers import SGD, Adam, Adamax, Adagrad, Nadam
from tensorflow.keras.constraints import MaxNorm
from tensorflow.keras.callbacks import EarlyStopping, History
from keras_self_attention import SeqSelfAttention
import wandb
from wandb.keras import WandbCallback
from sklearn.utils import shuffle
from statistics import mean
from human_id import generate_id
import os
import random
import pickle

# os.environ['WANDB_MODE'] = 'dryrun'

from cross_validation_generator import get_folds

utils = __import__('227_utils')

LEARNING_RATE = 5e-08  # 5e-09, 5e-08, 5e-07
BATCH_SIZE = 20
EPOCHS = 100
OPTIMIZER = "adamax"  # sdg, adam, adamax, adagrad, nadam
ACTIVATION_FUNC = "tanh"  # tanh, sigmoid
DROPOUT_RATE = 0.5
CROSS_VAL = 10
ES_PATIENCE = 2
LOSS = "mean_squared_error"
USE_LSTM = False
FEATURE_TYPE = "feature-streams"  # embeddings-ge2e, embeddings-trill, feature-streams (embeddings dir name)
FEATURE_DIR = "split-10"  # split-10, ... (subdir name in ./wavs)

seed = random.randint(0, 100000)
print(f'Seed: {seed}')

generator = get_folds(FEATURE_TYPE, FEATURE_DIR, USE_LSTM, CROSS_VAL, seed=seed)  # seed=21
run_name = generate_id(word_count=3)

print(f"Starting run {run_name} ...")

best_loss_per_fold = []
predictions = []
truths = []

for i in range(1, CROSS_VAL + 1):
    # run = wandb.init(
    #     config={"learning_rate": LEARNING_RATE,
    #             "batch size": BATCH_SIZE,
    #             "epochs": EPOCHS,
    #             "optimizer": OPTIMIZER,
    #             "activation_func": ACTIVATION_FUNC,
    #             "dropout_rate": DROPOUT_RATE,
    #             "cross_validation": CROSS_VAL,
    #             "loss": LOSS,
    #             "feature_type": FEATURE_TYPE,
    #             "feature_dir": FEATURE_DIR},
    #     project="SQE-quality",
    #     reinit=True,
    #     name=f"{run_name}-{i}/{CROSS_VAL}"
    # )

    os.system('krenew')

    print('--------------------------------')
    print(f"Starting cross validation {i}/{CROSS_VAL}")
    print('--------------------------------\n')

    # with run:
    x_train, y_train, x_val, y_val = next(generator)

    print(f'Created folds for iteration {i}')

    x_train = np.array(x_train)
    x_val = np.array(x_val)
    y_train = np.array(y_train)
    y_val = np.array(y_val)

    x_train, y_train = shuffle(x_train, y_train)

    model = Sequential()
    if FEATURE_TYPE == 'embeddings-ge2e':
        model.add(Dense(256, input_dim=256))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
    elif FEATURE_TYPE == 'embeddings-trill':
        if USE_LSTM:
            model.add(Bidirectional(LSTM(2048, input_shape=(54, 2048), return_sequences=True), merge_mode='concat'))  # 54 timesteps, 2048 feature length per timestep
            model.add(SeqSelfAttention(attention_width=15,
                                       attention_activation=ACTIVATION_FUNC))  # attention width 15 * 200 ms = 3 seconds
        else:
            model.add(Dense(2048, input_dim=2048))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
        model.add(Dense(2048, kernel_constraint=MaxNorm(3)))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
        model.add(Dense(2048, kernel_constraint=MaxNorm(3)))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
        model.add(Dense(1024, kernel_constraint=MaxNorm(3)))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
        model.add(Dense(512, kernel_constraint=MaxNorm(3)))
        model.add(Activation(ACTIVATION_FUNC))
        model.add(Dropout(DROPOUT_RATE))
        model.add(Dense(256, kernel_constraint=MaxNorm(3)))
    elif FEATURE_TYPE == 'feature-streams':
        model.add(Bidirectional(LSTM(256, input_shape=(50, 50), return_sequences=True), merge_mode='concat'))  # first 50 is timesteps, second 50 is length of features
        model.add(SeqSelfAttention(attention_width=15,
                                   attention_activation=ACTIVATION_FUNC))  # attention width 15 * 200 ms = 3 seconds
    model.add(Activation(ACTIVATION_FUNC))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(256, kernel_constraint=MaxNorm(3)))
    model.add(Activation(ACTIVATION_FUNC))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(256, kernel_constraint=MaxNorm(3)))
    model.add(Activation(ACTIVATION_FUNC))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(128, kernel_constraint=MaxNorm(3)))
    model.add(Activation(ACTIVATION_FUNC))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Dense(64, kernel_constraint=MaxNorm(3)))
    model.add(Activation(ACTIVATION_FUNC))
    model.add(Dropout(DROPOUT_RATE))
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

    model.compile(loss=LOSS, optimizer=switcher.get(OPTIMIZER))

    print('Compiled model - starting training ...')

    # model.build((None, 2048, 54))  # TRILL
    # model.build((None, 50, None))  # audio feature streams
    # model.summary()
    #
    # exit()

    history = model.fit(
        x_train,
        y_train,
        # validation_split=VAL_SPLIT,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(x_val, y_val),
        callbacks=[# WandbCallback(),
                   EarlyStopping(
                       monitor='val_loss', min_delta=0, patience=ES_PATIENCE, verbose=0, mode='auto',
                       baseline=None, restore_best_weights=True
                   )]
    )

    print(f'History: {history.history}')
    best_loss_per_fold += [min(history.history['val_loss'])]
    print(best_loss_per_fold)
    print(f'Average best loss:{mean(best_loss_per_fold)}')

    prediction = model.predict(x_val)
    predictions += [prediction.flatten().tolist()]
    truths += [y_val.flatten().tolist()]

    # if i == CROSS_VAL:
    #     run.log({"avg_best_loss": mean(best_loss_per_fold)})

    # model.evaluate(x_val, y_val)

modelname = f"models/{FEATURE_TYPE}{'-LSTM' if USE_LSTM else ''}-{mean(best_loss_per_fold):.4f}-{run_name}"
model.save(modelname)
print(f'Saved last model as {modelname}')

predictionsname = f"predictions/{FEATURE_TYPE}{'-LSTM' if USE_LSTM else ''}-{mean(best_loss_per_fold):.4f}-{run_name}.pickle"
pickle.dump((predictions, truths), open(predictionsname, "wb"))
print(f'Saved predictions as {predictionsname}')

