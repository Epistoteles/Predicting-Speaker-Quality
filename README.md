# Predicting-Speaker-Quality

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

Welcome to __Predicting-Speaker-Quality__! This repository contains the code used for my Bachelor's thesis with the title _Predicting Speaker Quality Using Embeddings_. All of it is research code written by an inexperienced undergraduate student, so please don't expect perfect documentation. However, if you run into any troubles or even want to improve or add to the code base, don't hesitate to reach out to me. Found a mistake? Let me know as well.

Besides just reading this README file, a good idea to delve into the topic might also be to read the resulting thesis itself, which is included in this repository as `Predicting Speaker Quality Using Embeddings.pdf`.


## Setup

To set up the project, follow these steps:

#### 1. Getting Started

* Clone this repository.
* Install the requirements from `requiremente.txt` using `pip install -r requirements.txt` if they are not already satisfied. If you like, you can do this in a virtual environment to keep things tidy.

#### 2. Getting and Creating Data

* Download the Spoken Wikipedia Corpus (German, with audio) from https://nats.gitlab.io/swc/ and replace the directory `german` with it.
* Navigate into the main project directory and execute the `split.sh` script using `bash split.sh -m 10 -d 10 -p`, which will generate up to 10 samples of length 10 seconds from each audio file in the `wavs` directory and its subdirectories. This may take a while. To see all available options, type `bash split.sh -h`.
* Generate the GE2E and TRILL embeddings by running the `update_embeddings.py` script once. If you want to create new embeddings, for example because you have new .wav files in your demo folder, just run it again. It will remember which embeddings have already been created and delete embeddings that are no longer needed.
* Navigate into the `feature-scripts` directory and execute the `update_audio_features.sh` script using `bash update_audio_features.sh`. Just like the previous script, this one does all the bookkeeping for you and tracks new and deleted .wav files.

## Training and Evaluating Models

* In order to train and evaluate the neural network models (DNNs and LSTMs), simply run the `keras_regressors.py` script. All parameters like network architecture, learning rate, etc. can be modified inside the file itself.
* For the kNN and random forest regressor, use the `sklearn_regressors.py` file. Like before, all parameters can be set inside the script itself.

## (Re-)Creating Plots

If you want to create plots from the resulting predictions (just like the ones seen in the thesis), take a look at the individual plotting scripts inside `plot-scripts`.