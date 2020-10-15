# Speech-Quality-Estimation

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

## Setup

To setup this project, follow the following steps:

### 1. Getting and generating all files

* Clone this repository locally
* Download the Spoken Wikipedia Corpus (German, with audio) from https://nats.gitlab.io/swc/ and replace the directory `german` with it
* Navigate into the main project directory and execute the `split.sh` script using `bash split.sh -m 10 -d 10 -p`, which will generate up to 10 samples of length 10 seconds from each audio file in the `wavs` directory and its subdirectories. This may take a while. To see all available options, type `bash split.sh -h`.
* Generate ...
