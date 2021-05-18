import matplotlib.pyplot as plt
import random
import seaborn as sns


rankings = [96, 106, 197, 51, 190, 143, 70, 205, 143, 179, 3, 24, 108, 209, 43, 100, 144, 171, 178, 27, 2, 73, 204, 79, 73, 90, 54, 24, 96, 202, 182, 183, 224, 126, 83, 53, 214, 218, 148, 123, 189, 167, 123, 171, 17, 207, 70, 8, 193, 48, 166, 216, 193, 71, 57, 45, 210, 34, 151, 57, 82, 178, 89, 110, 32, 133, 9, 18, 120, 154, 133, 129, 32, 148, 223, 86, 119, 108, 45, 86, 100, 165, 187, 109, 141, 175, 69, 45, 150, 142, 71, 52, 23, 28, 132, 115, 213, 4, 203, 106, 84, 126, 61, 61, 113, 41, 192, 150, 140, 39, 218, 226, 140, 162, 13, 92, 191, 80, 26, 179, 160, 116, 39, 118, 127, 186, 61, 36, 167, 221, 82, 99, 192, 50, 48, 160, 151, 169, 16, 110, 45, 6, 192, 186, 105, 57, 11, 147, 63, 91, 158, 68, 155, 129, 1, 166, 109, 222, 67, 9, 134, 153, 16, 84, 96, 218, 206, 21, 58, 81, 208, 173, 178, 19, 200, 44, 125, 143, 41, 139, 169, 122, 129, 169, 203, 42, 175, 208, 179, 0, 132, 160, 78, 91, 97, 30, 89, 75, 13, 188, 29, 65, 72, 156, 12, 133, 29, 114, 27, 104, 214, 196, 212, 93, 97, 36, 9, 220, 71, 53, 22, 201, 179, 5, 141, 118, 225]
num_of_speakers = len(rankings)


def get_ranking_distance(rating):
    rank_a = rankings[rating[0]]
    rank_b = rankings[rating[1]]
    return abs(rank_a - rank_b) / num_of_speakers


random_ranking_diffs = list(map(lambda x: get_ranking_distance(x), [x for x in [[random.randint(0, 226), random.randint(0, 226)] for i in range(9000)] if (x[0] != x[1])]))
plt.figure(figsize=(10, 7))
sns.set_style("darkgrid")
plt.xticks([0, 0.25, 0.5, 0.75, 1])
plt.yticks([0, 200, 400, 600, 800, 1000])
plt.xlim(-0.05, 1.05)
plt.ylim(0, 900)
plt.hist(random_ranking_diffs, bins=25)
plt.title("Ranking distances of ratings using random sampling", fontsize=15)
plt.axvline(x=0.25, color="deepskyblue")
plt.text(0.26, 730, "> 0.25\n" + "%.2f" % (sum(1 for i in random_ranking_diffs if i > .25) / len(random_ranking_diffs) * 100) + "%", color="black")
plt.axvline(x=0.5, color="deepskyblue")
plt.text(0.51, 730, "> 0.5\n" + "%.2f" % (sum(1 for i in random_ranking_diffs if i > .5) / len(random_ranking_diffs) * 100) + "%", color="black")
plt.xlabel('ranking distance')
plt.ylabel('count')
plt.savefig('../graphics/plots/sampling_random.png', dpi=300)
plt.close()
