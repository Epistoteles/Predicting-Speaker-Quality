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
# Audio features avg DNN
data2 = [0.061731915920972824, 0.10756511986255646, 0.06044911965727806, 0.15233802795410156, 0.09755758196115494,
         0.07012870162725449, 0.06547956168651581, 0.06958449631929398, 0.09162595123052597, 0.08986470103263855]
# Audio features avg kNN
data3 = [0.045703873599793034, 0.08664236493432023, 0.06899124764695606, 0.06693418533237244, 0.08116156976269454,
         0.07021935867828472, 0.07270238603504822, 0.10340324497422189, 0.07430864173572164, 0.06220724781632232]
# Audio features avg RF
data4 = [0.057323054558494936, 0.10666203112784328, 0.05767030872766399, 0.05937494939078073, 0.07595945434916127,
         0.08569087312119177, 0.06879955346574372, 0.09331497888997778, 0.06590029614662794, 0.06303317446231883]
# GE2E embeddings DNN
data5 = [0.04590533301234245, 0.0962676852941513, 0.05905873328447342, 0.07357267290353775, 0.07044863700866699,
         0.06663740426301956, 0.0677716560125351, 0.09596561640501022, 0.07816271483898163, 0.0585385337471962]
# GE2E embeddings kNN
data6 = [0.04049301527117979, 0.07102846899118305, 0.05436658795874397, 0.04933381119695701, 0.07038662074548023,
         0.06891040740585433, 0.05667604010507231, 0.07109557296413592, 0.05864453547701708, 0.05676925645498431]
# GE2E embeddings RF
data7 = [0.07024132670040377, 0.058908436227460934, 0.06351506117754409, 0.05734822399331674, 0.07490406103264607,
         0.0683951805979813, 0.057184301581472086, 0.05574969152486769, 0.05868769940806914, 0.05372622729056869]
# TRILL embeddings LSTM  Learning rate 5e-09, Dropout 0.5, Batch size 50,
data8 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]
# TRILL embeddings average DNN
data9 = [0.055929217487573624, 0.06091725453734398, 0.0757758617401123, 0.0648883581161499, 0.09531573951244354,
         0.08139252662658691, 0.07454532384872437, 0.07128109037876129, 0.0831625759601593, 0.05294238030910492]
# TRILL embeddings average kNN
data10 = [0.050259927468954566, 0.09222961387001387, 0.05755647567168368, 0.06322380106201954, 0.06823415798587272,
          0.0640257835812705, 0.07348951232931608, 0.09100876293337316, 0.06994578309884429, 0.07100591255846651]
# TRILL embeddings average RF
data11 = [0.0688362891055638, 0.09025336603154398, 0.07685740386506298, 0.06958175315579791, 0.06355758812160088,
          0.07205341553314332, 0.0879793656832923, 0.06998428170862019, 0.0754743959244977, 0.06721214912029502]


data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11]

# set up plot
plt.figure(figsize=(14, 9))
sns.set_style("darkgrid")
# plt.title(f"Mean squared error for 10 folds per feature and learning method")

# define and set ticks
ticks = ['audio features\nBi-LSTM + Att.',
         'audio features\navg. DNN',
         'audio features\navg. kNN',
         'audio features\navg. RF',
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
plt.ylim(0, 0.18)
plt.xlim(0.5, 11.5)

# plot data
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'),
                      showmeans=False,
                      meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='black'))

# plot ticks again because they disappeared
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], labels=ticks, fontsize=8)

# define and set RGB colors
colors_dark = ['#ff9900ff'] * 4 + ['#1155ccff'] * 3 + ['#38761dff'] * 4
colors_light = ['#fce5cdff'] * 4 + ['#c9daf8ff'] * 3 + ['#d9ead3ff'] * 4
for i, box in enumerate(boxplot['boxes']):
    # change outline color
    box.set(color=colors_light[i], linewidth=1)
    # change fill color
    box.set(facecolor=colors_light[i])
    plt.plot(i+1, mean(data[i]), marker='D', color=colors_dark[i], zorder=10)

# plot average legend
plt.plot(1.3, 0.01, marker='D', color='black')
plt.text(1.45, 0.01, '= avg.', fontsize=8, verticalalignment='center')

# plot outlier legend
plt.plot(2.2, 0.01, marker='o', markeredgecolor='black', markerfacecolor='.9')
plt.text(2.35, 0.01, '= outlier', fontsize=8, verticalalignment='center')

# plot true baselines
plt.axhline(y=0.1569, color='dimgrey', linestyle='--', linewidth=1)
plt.text(3, 0.1569 - 0.005, f"random guessing", color='dimgrey', horizontalalignment='center', fontsize=8)
plt.axhline(y=0.0627, color='dimgrey', linestyle='--', linewidth=1)
plt.text(3, 0.0627 - 0.007, f"mediocrity guessing", color='dimgrey', horizontalalignment='center', fontsize=8)

# save plot
plt.savefig('../plots/boxplots_exp_2_thesis.png', bbox_inches='tight', dpi=300)
plt.close()
