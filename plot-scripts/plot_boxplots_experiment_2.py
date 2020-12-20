import matplotlib.pyplot as plt
from statistics import median

# define and set title
title = 'Mean squared error for 10-fold cross-validation of individual prediction'
plt.title(title, fontsize=9)

# define data
# Audio features Bi-LSTM with attention
data1 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# GE2E embeddings
data2 = [0.04514303430914879, 0.10024463385343552, 0.07115302979946136, 0.07010502368211746, 0.07582344114780426,
         0.07056988775730133, 0.06817390024662018, 0.08700336515903473, 0.05894548073410988, 0.05538760870695114]
# TRILL embeddings average
data3 = [0.04465020075440407, 0.07901230454444885, 0.06730912625789642, 0.0618673712015152, 0.0826241746544838,
         0.06034095212817192, 0.07124308496713638, 0.11350255459547043, 0.07670380175113678, 0.06114530563354492]
# TRILL embeddings LSTM  Learning rate 5e-09, Dropout 0.5, Batch size 50,
data4 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]


data = [data1, data2, data3, data4]

# plot data
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'),
                      showmeans=True,
                      meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='black'))

# define and set ticks
ticks = ['Audio Features Bi-LSTM', 'GE2E Embeddings', 'TRILL Embeddings Avg.', 'TRILL Embeddings Bi-LSTM']
plt.xticks([1, 2, 3, 4], labels=ticks, fontsize=7)
plt.yticks(fontsize=7)

# define and set axis labels
plt.xlabel('')
plt.ylabel('accuracy', fontsize=8)

# define and set RGB colors
colors = [(0.9, 0.5, 0.3), (0.3, 0.7, 0.9), (0.3, 0.9, 0.5), (0.2, 0.7, 0.4)]
for i, box in enumerate(boxplot['boxes']):
    # change outline color
    box.set(color=colors[i], linewidth=1)
    # change fill color
    box.set(facecolor=colors[i])

# draw baseline
# plt.axhline(y=median(data1), color=colors[0], linestyle='--')
plt.axhline(y=0.1666, color='red', linestyle='--')
plt.axhline(y=0.0833, color='red', linestyle='--')
plt.axhline(y=0.07564, color='red', linestyle='--')

# make y axis start at 0
plt.ylim(ymin=0)

# save plot
plt.savefig('../graphics/plots/boxplots_exp_2.png', dpi=300)
plt.close()
