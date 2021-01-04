from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from cross_validation_generator import get_folds
from human_id import generate_id
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
import pickle
from statistics import mean

CROSS_VAL = 10
FEATURE_TYPE = "feature-streams"  # embeddings-ge2e, embeddings-trill, feature-streams (embeddings dir name)
FEATURE_DIR = "split-10"  # split-10, ... (subdir name in ./wavs)
METHOD = 'KNN'  # KNN, RF


def predict(save_predictions=False, n_neighbors=310, max_depth=20):
    generator = get_folds(FEATURE_TYPE, FEATURE_DIR, timeseries=False, folds=CROSS_VAL, seed=21)
    run_name = generate_id(word_count=3)

    print(f"Starting run {run_name}-{METHOD} ...")

    acc_per_fold = []
    predictions = []
    truths = []

    for i in range(1, CROSS_VAL + 1):
        start_message = f"Starting cross validation {i}/{CROSS_VAL} for param {'k=' + str(n_neighbors) if METHOD == 'KNN' else 'max_depth=' + str(max_depth)}"
        print('-'*len(start_message))
        print(start_message)
        print('-'*len(start_message))

        x_train, y_train, x_val, y_val = next(generator)

        print(f'Created folds for iteration {i}')

        x_train = np.array(x_train)
        x_val = np.array(x_val)
        y_train = np.rint(y_train)
        y_val = np.rint(y_val)

        x_train, y_train = shuffle(x_train, y_train)

        if METHOD == 'KNN':
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(x_train, y_train)
            prediction = knn.predict(x_val)
        elif METHOD == 'RF':
            rf = RandomForestClassifier(max_depth=max_depth)
            rf.fit(x_train, y_train)
            prediction = rf.predict(x_val)

        # acc = accuracy_score(y_val, prediction)
        acc = accuracy_score(y_val, np.random.randint(2, size=len(y_val)))  # replace predictions by random classes to simulate random guessing

        print(f'Accuracy for fold {i}: {acc}\n')

        predictions += [prediction.flatten().tolist()]
        acc_per_fold += [acc]
        truths += [y_val.flatten().tolist()]

    avg_loss = mean(acc_per_fold)
    result = f"| Average accuracy for {'k=' + str(n_neighbors) if METHOD == 'KNN' else 'max_depth=' + str(max_depth)}: {avg_loss} |"
    print(f'Accuracy per fold: {acc_per_fold}')
    print()
    print('-'*len(result))
    print(result)
    print('-'*len(result))

    if save_predictions:
        predictionsname = f"predictions/{FEATURE_TYPE}-{METHOD}-{avg_loss:.4f}-{run_name}.pickle"
        pickle.dump((predictions, truths), open(predictionsname, "wb"))
        print(f'Saved predictions as {predictionsname}')

    return avg_loss


def hyperparameter_search(start, end, stride):
    print(f'Hyperparameter search for {METHOD} from {start} to {end} in steps of {stride}')
    params = []
    loss_per_param = []
    for p in range(start, end+stride, stride):  # (10, 1010, 10) for k hyperparameter search from 10 to 1000 in steps of 10
        print(f'\n\nParameter: {p}/{end}')
        avg_acc = predict(n_neighbors=p) if METHOD == 'KNN' else predict(max_depth=p)
        params += [p]
        loss_per_param += [avg_acc]
    print(params)
    print(loss_per_param)

#predict(max_depth=6)
predict(n_neighbors=310)

# hyperparameter_search(4, 120, 4)
