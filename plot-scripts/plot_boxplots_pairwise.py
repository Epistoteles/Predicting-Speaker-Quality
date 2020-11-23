import matplotlib.pyplot as plt
from statistics import median

# define and set title
title = 'Pairwise prediction accuracy for 10-fold cross-validation'
plt.title(title)

# define data
data1 = [30, 45, 46, 35, 59, 67, 23, 75, 45, 65]
data2 = [70, 77, 84, 34, 56, 75, 80, 48, 55, 54]
data3 = [30, 40, 50, 70, 77, 82, 55, 65, 45, 50]
data = [data1, data2, data3]

# plot data
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'))

# define and set ticks
ticks = ['Audio Features', 'GE2E', 'TRILL']
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
