#!/bin/sh

python3 ./lightning-text-classification/training.py \
    --gpus 1 \
    --encoder_model bert-large-uncased \
    --train_csv data/preprocessed/A-train.pre
