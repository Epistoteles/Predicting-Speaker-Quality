import matplotlib.pyplot as plt
from statistics import median

# define and set title
title = 'Discrete prediction MSE for 10-fold cross-validation'
plt.title(title)

# define data
# Audio features Bi-LSTM with attention
data1 = [0.056874338537454605, 0.1377364993095398, 0.0852215588092804, 0.08032683283090591, 0.10063298046588898,
         0.05689895153045654, 0.09905548393726349, 0.10189623385667801, 0.10565530508756638, 0.07465212047100067]
# GE2E embeddings
data2 = [0.049740981310606, 0.09591852873563766, 0.06659960746765137, 0.05881047621369362, 0.06881038099527359,
         0.06587890535593033, 0.07302136719226837, 0.11443723738193512, 0.0910637229681015, 0.06586269289255142]
# TRILL embeddings average
data3 = [0.1782779097557068, 0.09736426919698715, 0.07286163419485092, 0.07695775479078293, 0.08534342795610428,
         0.07305404543876648, 0.07507871091365814, 0.1156117394566536, 0.07184602320194244, 0.06726393848657608]
# TRILL embeddings LSTM  Learning rate 5e-09, Dropout 0.5, Batch size 50,
data4 = [0.04521876573562622, 0.08845867216587067, 0.07183481752872467, 0.06727518141269684, 0.07924636453390121,
         0.0628887414932251, 0.07449563592672348, 0.09885834902524948, 0.07701925188302994, 0.0644703134894371]


data = [data1, data2, data3, data4]

# plot data
boxplot = plt.boxplot(data,
                      patch_artist=True,
                      medianprops=dict(color='black'))

# define and set ticks
ticks = ['Audio Features Bi-LSTM', 'GE2E Embeddings', 'TRILL Embeddings Avg.', 'TRILL Embeddings Bi-LSTM']
plt.xticks([1, 2, 3, 4], labels=ticks)

# define and set axis labels
plt.xlabel('')
plt.ylabel('accuracy')

# define and set RGB colors
colors = [(0.9, 0.5, 0.3), (0.3, 0.7, 0.9), (0.3, 0.9, 0.5), (0.25, 0.85, 0.45)]
for i, box in enumerate(boxplot['boxes']):
    # change outline color
    box.set(color=colors[i], linewidth=1)
    # change fill color
    box.set(facecolor=colors[i])

# draw baseline
# plt.axhline(y=median(data1), color=colors[0], linestyle='--')
plt.axhline(y=0.1, color=colors[0], linestyle='--')

# make y axis start at 0
plt.ylim(ymin=0)

# save plot
plt.show()
#plt.savefig('../graphics/plots/boxplots_exp_2.png', dpi=300)
#plt.close()
