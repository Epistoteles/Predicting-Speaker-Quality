from matplotlib import pyplot as plt
import seaborn as sns

labels = ['audio-Bi-LSTM', 'audio-DNN', 'audio-kNN', 'audio-RF', 'GE2E-DNN', 'GE2E-kNN', 'GE2E-RF', 'TRILL-Bi-LSTM',
          'TRILL-DNN', 'TRILL-kNN', 'TRILL-RF']
x_offsets = [-0.0006, -0.0006, 0, 0.0002, -0.0006, 0, 0, -0.0006, -0.0001, -0.0008, 0]
y_offsets = [0, 0, 0, -0.02, 0, 0, 0, 0, 0, -0.02, 0]
haligns = ['right', 'right', 'left', 'left', 'right', 'left', 'left', 'right', 'left', 'right', 'left']
default_x_offset = 0.0003
default_y_offset = 0.01
sd_sds = [0.723261371889488, 0.6633410330352938, 0.5494585244278477, 0.5361655252725409, 0.48328049393806133,
          0.3934145197048655, 0.4807015267451155, 0.5360884444682269, 0.47957007834242565, 0.46769581452109815,
          0.441956310051899]
mses = [0.08989503048360348, 0.08663251772522926, 0.07322741205157351, 0.07337286742398043, 0.07123289867699147,
        0.0597704316570608, 0.06186602095343305, 0.07297660931944847, 0.07161503285169601, 0.07009797305598149,
        0.0741790008249418]

plt.figure(figsize=(8, 8))
sns.set_style('darkgrid')
# plt.xlim(0, 0.1)
plt.ylim(0, 1)
plt.scatter(mses, sd_sds)
for i, txt in enumerate(labels):
    plt.annotate(txt, (mses[i] + x_offsets[i] + default_x_offset, sd_sds[i] + y_offsets[i] + default_y_offset), ha=haligns[i])
plt.title('')
plt.xlabel('mean squared error')
plt.ylabel('intra-inter-ratio')
plt.legend('')  # (loc='upper left')
plt.savefig(f"../graphics/plots/sd-sd-ratio-to-mse-scatterplot.png", dpi=300, bbox_inches='tight', pad_inches=0)
plt.close()
