from encoder import inference as encoder
from pathlib import Path
import os
import pickle
from tqdm import tqdm


def create_embedding(path):
    in_fpath = Path(path.replace("\"", "").replace("\'", ""))
    preprocessed_wav = encoder.preprocess_wav(in_fpath)
    return encoder.embed_utterance(preprocessed_wav)


encoder.load_model(Path("encoder/saved_models/pretrained.pt"))

dir_to_update = "wavs"

wavs_total = 0

for root, dirs, files in os.walk(dir_to_update):
    wavs_total += len(files)

print()
print("🔊 There are {0} .wav files inside {1}.".format(wavs_total, dir_to_update))
print("Updating embeddings ...")
print()

embeddings_not_modified = 0
embeddings_deleted = 0
embeddings_created = 0

# Remove outdated embeddings with no matching source in wavs
for root, dirs, files in os.walk("embeddings", topdown=False):
    for f in files:
        embedding = os.path.join(root, f)
        wav = embedding.replace("embeddings/", "wavs/").replace(".p", ".wav")
        if not os.path.exists(wav):
            os.remove(embedding)
    for d in dirs:
        embedding_dir = os.path.join(root, d)
        wav_dir = embedding_dir.replace("embeddings/", "wavs/")
        if not os.path.exists(wav_dir):
            os.rmdir(embedding_dir)

# Then create new embeddings for all .wav files that don't already have one
progressbar = tqdm(total=wavs_total)
for root, dirs, files in os.walk(dir_to_update):
    for d in dirs:
        directory = os.path.join(root, d).replace("wavs/", "embeddings/")
        if not os.path.isdir(directory):
            os.makedirs(directory)
    for f in files:
        wav_path = os.path.join(root, f)
        if wav_path.endswith(".wav"):
            embedding_path = wav_path.replace("wavs/", "embeddings/").replace(".wav", ".p")
            if os.path.isfile(embedding_path):
                embeddings_not_modified += 1
            else:
                embedding = create_embedding(wav_path)
                pickle.dump(embedding, open(embedding_path, "wb"))
                embeddings_created += 1
            progressbar.update(1)
progressbar.close()

print()
print("✔️ Done")
print("{0} embeddings not modified, {1} deleted, {2} created"
      .format(embeddings_not_modified, embeddings_deleted, embeddings_created))
