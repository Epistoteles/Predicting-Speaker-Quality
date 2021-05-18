import matplotlib.pyplot as plt
import csv
import numpy as np
from keras_classifier import get_ranking_distance, predict_based_on_ranking


with open('../ratings.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

data = list(map(lambda r: list(map(lambda i: int(i), r)), data))


count = [0.0]*25
agreed = [0.0]*25
for d in data:
    hist_bin = int(get_ranking_distance(d)*25)
    count[hist_bin] += 1
    if predict_based_on_ranking(d) == d[2]:
        agreed[hist_bin] += 1

agreement_proportions = np.array(agreed) / np.array(count)

plt.bar(np.array(list(range(25)))/25, agreement_proportions, width=0.04)
plt.title("Agreement with general ranking by rating distance", fontsize=15)
plt.axvline(x=0.25, color="red")
plt.axvline(x=0.5, color="red")
plt.savefig('plots/ranking_agreement.png', dpi=300)
plt.close()