import matplotlib.pyplot as plt
from statistics import median, mean
import seaborn as sns

# define and set title
title = 'Mean squared error for 10-fold cross-validation of individual prediction'
plt.title(title, fontsize=9)

# define data
# Audio features Bi-LSTM with attention
data1 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# Audio features avg DNN WRONG
data2 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# Audio features avg kNN WRONG
data3 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# Audio features avg RF WRONG
data4 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# GE2E embeddings DNN
data5 = [0.04590533301234245, 0.0962676852941513, 0.05905873328447342, 0.07357267290353775, 0.07044863700866699,
         0.06663740426301956, 0.0677716560125351, 0.09596561640501022, 0.07816271483898163, 0.0585385337471962]
# GE2E embeddings kNN  WRONG
data6 = [0.04590533301234245, 0.0962676852941513, 0.05905873328447342, 0.07357267290353775, 0.07044863700866699,
         0.06663740426301956, 0.0677716560125351, 0.09596561640501022, 0.07816271483898163, 0.0585385337471962]
# GE2E embeddings RF  WRONG
data7 = [0.04590533301234245, 0.0962676852941513, 0.05905873328447342, 0.07357267290353775, 0.07044863700866699,
         0.06663740426301956, 0.0677716560125351, 0.09596561640501022, 0.07816271483898163, 0.0585385337471962]
# TRILL embeddings LSTM  Learning rate 5e-09, Dropout 0.5, Batch size 50,
data8 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]
# TRILL embeddings average DNN
data9 = [0.055929217487573624, 0.06091725453734398, 0.0757758617401123, 0.0648883581161499, 0.09531573951244354,
         0.08139252662658691, 0.07454532384872437, 0.07128109037876129, 0.0831625759601593, 0.05294238030910492]
# TRILL embeddings average kNN WRONG
data10 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]
# TRILL embeddings average RF WRONG
data11 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]

data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11]

# plot data
plt.figure(figsize=(14, 7))
sns.set_style("darkgrid")
plt.title(f"Mean squared error for 10 folds per feature and approach")
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'),
                      showmeans=False,
                      meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='black'))

# define and set ticks
ticks = ['Audio Features\nBi-LSTM + Att.',
         'Audio Features\navg. DNN',
         'Audio Features\navg. kNN',
         'Audio Features\navg. RF',
         'GE2E DNN',
         'GE2E kNN',
         'GE2E RF',
         'TRILL\nBi-LSTM + Att.',
         'TRILL avg. DNN',
         'TRILL avg. kNN',
         'TRILL avg. RF']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], labels=ticks, fontsize=8)

# define and set axis labels
plt.xlabel('')
plt.ylabel('mean squared error')

# define and set RGB colors
colors_dark = ['#ff9900ff'] * 4 + ['#1155ccff'] * 3 + ['#38761dff'] * 4
colors_light = ['#fce5cdff'] * 4 + ['#c9daf8ff'] * 3 + ['#d9ead3ff'] * 4
for i, box in enumerate(boxplot['boxes']):
    # change outline color
    box.set(color=colors_light[i], linewidth=1)
    # change fill color
    box.set(facecolor=colors_light[i])
    plt.plot(i+1, mean(data[i]), marker='D', color=colors_dark[i], zorder=10)

# draw baseline
plt.axhline(y=0.1666, color='red', linestyle='--', linewidth=1)
plt.text(3.5, 0.1666 - 0.005, f"'random guessing' baseline", color='red', horizontalalignment='center', fontsize=8)
plt.axhline(y=0.0833, color='red', linestyle='--', linewidth=1)
plt.text(3.5, 0.0833 + 0.002, f"'always guess 0.5' baseline", color='red', horizontalalignment='center', fontsize=8)
plt.axhline(y=0.0627, color='red', linestyle='--', linewidth=1)
plt.text(3.5, 0.0627 - 0.005, f"true 'always guess 0.5' baseline", color='red', horizontalalignment='center', fontsize=8)
plt.plot(0.67, 0.01, marker='D', color='black')
plt.text(0.72, 0.01, '= avg.', fontsize=8, verticalalignment='center')

# make y axis start at 0
plt.ylim(ymin=0)

# save plot
plt.savefig('../graphics/plots/boxplots_exp_2.png', dpi=300)
plt.close()
