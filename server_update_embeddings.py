#!/usr/bin/env python
from encoder import inference as encoder
from pathlib import Path
import os
import pickle

EMBEDDING_TYPE = "ge2e"

def create_embedding(path):
    in_fpath = Path(path.replace("\"", "").replace("\'", ""))
    preprocessed_wav = encoder.preprocess_wav(in_fpath)
    return encoder.embed_utterance(preprocessed_wav)

def update_embeddings():
    encoder.load_model(Path("encoder/saved_models/pretrained.pt"))
    input_dir = "uploads"
    for file in os.listdir(input_dir):
        wav_path = os.path.join(input_dir, file)
        if wav_path.endswith(".wav"):
            embedding_path = wav_path.replace(f"{input_dir}/", f"embeddings-{EMBEDDING_TYPE}/").replace(".wav", ".pickle")
            embedding = create_embedding(wav_path)
            pickle.dump(embedding, open(embedding_path, "wb"))
