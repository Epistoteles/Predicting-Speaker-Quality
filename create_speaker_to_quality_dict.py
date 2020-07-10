import pickle
import os

speakers = pickle.load(open("227_speakers.pickle", "rb"))
ranks = pickle.load(open("227_ranks.pickle", "rb"))

quality = {}

for d in os.listdir("embeddings/split-10"):
    if d in speakers:
        rank = ranks[speakers.index(d)]
        quality[d] = rank / 227.0
    else:
        quality[d] = -1

print(quality)

pickle.dump(quality, open("speaker_to_quality_dict.pickle", "wb"))
