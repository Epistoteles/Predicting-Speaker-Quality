from tensorflow.keras.utils import Sequence
import numpy as np
import pickle


class Stream_Generator(Sequence):

    def __init__(self, filenames, labels, batch_size, type):
        self.filenames = filenames
        self.labels = labels
        self.batch_size = batch_size

    def __len__(self):
        return (np.ceil(len(self.filenames) / float(self.batch_size))).astype(np.int)

    def __getitem__(self, batch):
        batch_x = self.filenames[batch * self.batch_size: (batch + 1) * self.batch_size]
        batch_y = self.labels[batch * self.batch_size: (batch + 1) * self.batch_size]

        # trill embeddings
        if type(self.filenames[0]) is str:
            batch_x = [pickle.load(open(x, 'rb')) for x in batch_x]
        # feature streams
        else:
            batch_x = [list(map(lambda x: pickle.load(open(x, 'rb')), sublist)) for sublist in batch_x]

        return np.array([
            np.array(batch_x), np.array(batch_y)
        ])
