import sys
import os
import pickle
import numpy as np
import server_update_embeddings

filename = sys.argv[1]

server_update_embeddings.update_embeddings()

feature_type = "ge2e"

feature = pickle.load(open(os.path.join(f'embeddings-{feature_type}/', filename.replace(".wav", ".pickle"), 'rb')))

models = os.listdir('models/')
models = sorted([m for m in models if m.startswith(f"{feature_type}-0")],
                key=lambda x: float(x.split('-')[2]))
model = models[0]
model = pickle.load(open(f"models/{model}", 'rb'))

feature = feature.transpose()
prediction = model.predict(np.array(feature).reshape(1, -1))
prediction = int(prediction[0]*100)

sys.stdout.write(str(prediction))
