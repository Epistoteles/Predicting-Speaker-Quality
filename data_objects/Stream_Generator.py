from tensorflow.keras.utils import Sequence
import numpy as np

class Stream_Generator(Sequence):

    def __init__(self, filenames, labels, batch_size):
        self.filenames = filenames
        self.labels = labels
        self.batch_size = batch_size

    def __len__(self):
        return (np.ceil(len(self.filenames) / float(self.batch_size))).astype(np.int)

    def __getitem__(self, batch):
        batch_x = self.filenames[batch * self.batch_size: (batch + 1) * self.batch_size]
        batch_y = self.labels[batch * self.batch_size: (batch + 1) * self.batch_size]

        



        return np.array([
            resize(imread('/content/all_images/' + str(file_name)), (80, 80, 3))
            for file_name in batch_x]) / 255.0, np.array(batch_y)