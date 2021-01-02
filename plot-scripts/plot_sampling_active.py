import csv
import matplotlib.pyplot as plt
from keras_rating_classifier import get_ranking_distance
import seaborn as sns


with open('../ratings.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

data = list(map(lambda r: list(map(lambda i: int(i), r)), data))

ranking_diffs = list(map(lambda x: get_ranking_distance(x), data))
plt.figure(figsize=(10, 7))
sns.set_style("darkgrid")
plt.hist(ranking_diffs, bins=25)
plt.title("Distances of ratings using active sampling", fontsize=15)
plt.axvline(x=0.25, color="red")
plt.text(0.26, 800, "> 0.25\n" + "%.2f" % (sum(1 for i in ranking_diffs if i > .25) / len(ranking_diffs) * 100) + "%",
         color="red")
plt.axvline(x=0.5, color="red")
plt.text(0.51, 800, "> 0.5\n" + "%.2f" % (sum(1 for i in ranking_diffs if i > .5) / len(ranking_diffs) * 100) + "%",
         color="red")
plt.savefig('../graphics/plots/active_sampling.png', dpi=300)
plt.close()
