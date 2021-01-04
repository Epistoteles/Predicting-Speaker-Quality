from cross_validation_generator import get_folds
import numpy as np

generator = get_folds('feature-streams', 'split-10', timeseries=False, folds=10, seed=21)

x_train, y_train, x_val, y_val = next(generator)

x_train = np.array(x_train)
x_val = np.array(x_val)
y_train = np.rint(y_train)
y_val = np.rint(y_val)

print(x_val)
print(y_val)
print(len(x_val))
print(len(y_val))