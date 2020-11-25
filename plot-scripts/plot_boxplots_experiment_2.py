import matplotlib.pyplot as plt
from statistics import median

# define and set title
title = 'Discrete prediction accuracy for 10-fold cross-validation'
plt.title(title)

# define data
# audio features
data1 = [0.07855293899774551, 0.17478907108306885, 0.08146423101425171, 0.08806506544351578, 0.10416339337825775,
         0.10123932361602783, 0.09808984398841858, 0.1549820899963379, 0.13940401375293732, 0.10752617567777634]
# GE2E embeddings
data2 = [0.1211964413523674, 0.23287878930568695, 0.31405943632125854, 0.3469264805316925, 0.29702845215797424,
         0.18917779624462128, 0.27789291739463806, 0.3133980333805084, 0.14922665059566498, 0.20600064098834991]
# TRILL embeddings
data3 = []
data = [data1, data2, data3]

# plot data
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'))

# define and set ticks
ticks = ['Audio Features', 'GE2E Embeddings', 'TRILL Embeddings']
plt.xticks([1, 2, 3], labels=ticks)

# define and set axis labels
plt.xlabel('')
plt.ylabel('accuracy')

# define and set RGB colors
colors = [(0.9, 0.5, 0.3), (0.3, 0.7, 0.9), (0.3, 0.9, 0.5)]
for i, box in enumerate(boxplot['boxes']):
    # change outline color
    box.set(color=colors[i], linewidth=1)
    # change fill color
    box.set(facecolor=colors[i])

# draw baseline
plt.axhline(y=median(data1), color=colors[0], linestyle='--')

# make y axis start at 0
plt.ylim(ymin=0)

# show plot
plt.show()
