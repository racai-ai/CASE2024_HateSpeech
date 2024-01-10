#!/bin/sh

# TF-IDF - lemma, stop
python3 020_tfidf.py --train data/preprocessed/A-train.pre --test data/preprocessed/A-test.pre --out A-test --stop --lemma --pred
python3 make_submission.py --pred data/pred_tfidf/A-test.pred --base data/preprocessed/A-test.pre --out A-test-tfidf.json

# BERT
mkdir -p data/pred_bert-large
CUDA_VISIBLE_DEVICES="" python3 lightning-text-classification/predict.py \
    --input data/preprocessed/A-test.pre \
    --experiment data/bert-large-uncased-3e-05-2e-05/A-1 \
    --output data/pred_bert-large/A-test.pred
    #--experiment data/bert-large/A-5 \
    #--experiment data/bert-large-uncased-rte-1e-05-5e-05/A-5 \

python3 make_submission.py --pred data/pred_bert-large/A-test.pred --base data/preprocessed/A-test.pre --out A-test-bert.json

# DT
python3 080_prepare_data.py --base data/preprocessed/A-test.pre --pred1 data/pred_tfidf/A-test.pred --pred2 data/pred_bert-large/A-test.pred --out data/folds/A-test.combined
python3 090_decision_tree.py --train data/folds/A-5-test.combined --test data/folds/A-test.combined --out A-test --pred
python3 make_submission.py --pred data/pred_dt/A-test.pred --base data/preprocessed/A-test.pre --out A-test-dt.json
