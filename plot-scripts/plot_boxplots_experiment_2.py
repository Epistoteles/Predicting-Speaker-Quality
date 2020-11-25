import matplotlib.pyplot as plt
from statistics import median

# define and set title
title = 'Discrete prediction accuracy for 10-fold cross-validation'
plt.title(title)

# define data
# Audio features LSTM
data1 = [0.07855293899774551, 0.17478907108306885, 0.08146423101425171, 0.08806506544351578, 0.10416339337825775,
         0.10123932361602783, 0.09808984398841858, 0.1549820899963379, 0.13940401375293732, 0.10752617567777634]
# GE2E embeddings
data2 = [0.049740981310606, 0.09591852873563766, 0.06659960746765137, 0.05881047621369362, 0.06881038099527359,
         0.06587890535593033, 0.07302136719226837, 0.11443723738193512, 0.0910637229681015, 0.06586269289255142]
# TRILL embeddings average
data3 = [0.1782779097557068, 0.09736426919698715, 0.07286163419485092, 0.07695775479078293, 0.08534342795610428,
         0.07305404543876648, 0.07507871091365814, 0.1156117394566536, 0.07184602320194244, 0.06726393848657608]
# TRILL embeddings LSTM
data4 = []
data = [data1, data2, data3, data4]

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
