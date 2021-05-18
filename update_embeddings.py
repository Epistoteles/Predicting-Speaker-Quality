from encoder import inference as encoder
from pathlib import Path
import os
import pickle
from tqdm import tqdm
from scipy.io.wavfile import read
import tensorflow_hub as hub
import numpy as np
import sys
import tensorflow.compat.v2 as tf
tf.enable_v2_behavior()
assert tf.executing_eagerly()


EMBEDDING_TYPE = "trill"  # "ge2e" for GE2E, "trill" for trill


def create_embedding(path):
    if EMBEDDING_TYPE == "ge2e":
        in_fpath = Path(path.replace("\"", "").replace("\'", ""))
        preprocessed_wav = encoder.preprocess_wav(in_fpath)
        return encoder.embed_utterance(preprocessed_wav)
    else:
        # in_fpath = Path(path.replace("\"", "").replace("\'", ""))
        # preprocessed_wav = encoder.preprocess_wav(in_fpath)
        samplerate, data = read(path.replace("\"", "").replace("\'", ""))
        if samplerate != 16000:
            sys.exit(f"{path} does not have sample rate of 16000")
        emb = module(samples=np.array(data, dtype=float), sample_rate=16000)['embedding']
        emb.shape.assert_is_compatible_with([None, 2048])
        return emb.numpy()


if EMBEDDING_TYPE not in {"ge2e", "trill"}:
    sys.exit("Embedding type has to be 'ge2e' or 'trill'.")

encoder.load_model(Path("encoder/saved_models/pretrained.pt"))

if EMBEDDING_TYPE == "trill":
    module = hub.load('https://tfhub.dev/google/nonsemantic-speech-benchmark/trill-distilled/3')

dir_to_update = "wavs"

wavs_total = 0

for root, dirs, files in os.walk(dir_to_update):
    wavs_total += len(files)

print()
print(f"Updating {EMBEDDING_TYPE} type embeddings in directory embeddings-{EMBEDDING_TYPE}.")
print("🔊 There are {0} .wav files inside {1}.".format(wavs_total, dir_to_update))
print("Starting update ...")
print()

embeddings_not_modified = 0
embeddings_deleted = 0
embeddings_created = 0

# Remove outdated embeddings with no matching source in wavs
for root, dirs, files in os.walk(f"embeddings-{EMBEDDING_TYPE}", topdown=False):
    for f in files:
        embedding = os.path.join(root, f)
        wav = embedding.replace(f"embeddings-{EMBEDDING_TYPE}/", "wavs/").replace(".pickle", ".wav")
        if not os.path.exists(wav):
            os.remove(embedding)
    for d in dirs:
        embedding_dir = os.path.join(root, d)
        wav_dir = embedding_dir.replace(f"embeddings-{EMBEDDING_TYPE}/", "wavs/")
        if not os.path.exists(wav_dir):
            os.rmdir(embedding_dir)

# Then create new embeddings for all .wav files that don't already have one
progressbar = tqdm(total=wavs_total)
for root, dirs, files in os.walk(dir_to_update):
    for d in dirs:
        directory = os.path.join(root, d).replace("wavs/", f"embeddings-{EMBEDDING_TYPE}/")
        if not os.path.isdir(directory):
            os.makedirs(directory)
    for f in files:
        wav_path = os.path.join(root, f)
        if wav_path.endswith(".wav"):
            embedding_path = wav_path.replace("wavs/", f"embeddings-{EMBEDDING_TYPE}/").replace(".wav", ".pickle")
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



EMBEDDING_TYPE = "ge2e"  # "ge2e" for GE2E, "trill" for trill


def create_embedding(path):
    if EMBEDDING_TYPE == "ge2e":
        in_fpath = Path(path.replace("\"", "").replace("\'", ""))
        preprocessed_wav = encoder.preprocess_wav(in_fpath)
        return encoder.embed_utterance(preprocessed_wav)
    else:
        # in_fpath = Path(path.replace("\"", "").replace("\'", ""))
        # preprocessed_wav = encoder.preprocess_wav(in_fpath)
        samplerate, data = read(path.replace("\"", "").replace("\'", ""))
        if samplerate != 16000:
            sys.exit(f"{path} does not have sample rate of 16000")
        emb = module(samples=np.array(data, dtype=float), sample_rate=16000)['embedding']
        emb.shape.assert_is_compatible_with([None, 2048])
        return emb.numpy()


if EMBEDDING_TYPE not in {"ge2e", "trill"}:
    sys.exit("Embedding type has to be 'ge2e' or 'trill'.")

encoder.load_model(Path("encoder/saved_models/pretrained.pt"))

if EMBEDDING_TYPE == "trill":
    module = hub.load('https://tfhub.dev/google/nonsemantic-speech-benchmark/trill-distilled/3')

dir_to_update = "wavs"

wavs_total = 0

for root, dirs, files in os.walk(dir_to_update):
    wavs_total += len(files)

print()
print(f"Updating {EMBEDDING_TYPE} type embeddings in directory embeddings-{EMBEDDING_TYPE}.")
print("🔊 There are {0} .wav files inside {1}.".format(wavs_total, dir_to_update))
print("Starting update ...")
print()

embeddings_not_modified = 0
embeddings_deleted = 0
embeddings_created = 0

# Remove outdated embeddings with no matching source in wavs
for root, dirs, files in os.walk(f"embeddings-{EMBEDDING_TYPE}", topdown=False):
    for f in files:
        embedding = os.path.join(root, f)
        wav = embedding.replace(f"embeddings-{EMBEDDING_TYPE}/", "wavs/").replace(".pickle", ".wav")
        if not os.path.exists(wav):
            os.remove(embedding)
    for d in dirs:
        embedding_dir = os.path.join(root, d)
        wav_dir = embedding_dir.replace(f"embeddings-{EMBEDDING_TYPE}/", "wavs/")
        if not os.path.exists(wav_dir):
            os.rmdir(embedding_dir)

# Then create new embeddings for all .wav files that don't already have one
progressbar = tqdm(total=wavs_total)
for root, dirs, files in os.walk(dir_to_update):
    for d in dirs:
        directory = os.path.join(root, d).replace("wavs/", f"embeddings-{EMBEDDING_TYPE}/")
        if not os.path.isdir(directory):
            os.makedirs(directory)
    for f in files:
        wav_path = os.path.join(root, f)
        if wav_path.endswith(".wav"):
            embedding_path = wav_path.replace("wavs/", f"embeddings-{EMBEDDING_TYPE}/").replace(".wav", ".pickle")
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
