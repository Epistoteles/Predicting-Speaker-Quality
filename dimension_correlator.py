from cross_validation_generator import get_folds
from scipy.stats import pearsonr

CROSS_VAL = 10
FEATURE_TYPE = "embeddings-ge2e"  # embeddings-ge2e, embeddings-trill, feature-streams (dir name)
FEATURE_DIR = "split-10"  # split-10, ... (subdir name in ./wavs)

generator = get_folds(FEATURE_TYPE, FEATURE_DIR, timeseries=False, folds=CROSS_VAL, seed=21, return_sex=True)
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))
x_train, y_train, x_val, y_val, sex_train, sex_val = next(generator)
print('------')
print(len(x_val))

x = x_train + x_val
y = y_train + y_val
sex = sex_train + sex_val
sex_ints = [0 if x == "m" else 1 for x in sex]

quality_correlations = []
sex_correlations = []
for dimension in range(len(x[0])):
    dimension_subsample = [embedding[dimension] for embedding in x]
    quality_correlations += [pearsonr(dimension_subsample, y)[0]]
    sex_correlations += [pearsonr(dimension_subsample, sex_ints)[0]]


quality_correlations_no_nans = [0 if not x > -100 or not x < 100 else x for x in quality_correlations]
sex_correlations_no_nans = [0 if not x > -100 or not x < 100 else x for x in sex_correlations]


print(quality_correlations)
print(quality_correlations_no_nans)

sex_correlation = pearsonr(sex_ints, y)[0]
corr_correlation = pearsonr(quality_correlations_no_nans, sex_correlations_no_nans)[0]

print(f"Dimension to quality correlations: {quality_correlations}")
print(f"Most positive dimension to quality correlation: {max(quality_correlations)}, dimension {quality_correlations.index(max(quality_correlations))}")
print(f"Most negative dimension to quality correlation: {min(quality_correlations)}, dimension {quality_correlations.index(min(quality_correlations))}")
print()
print(f"Dimension to sex correlations: {sex_correlations}")
print(f"Most positive dimension to sex correlation: {max(sex_correlations)}, dimension {sex_correlations.index(max(sex_correlations))}")
print(f"Most negative dimension to sex correlation: {min(sex_correlations)}, dimension {sex_correlations.index(min(sex_correlations))}")
print()
print(f"Sex to quality correlation: {sex_correlation}")
print()
print(f"dim2qual 2 dim2sex correlation: {corr_correlation}")
