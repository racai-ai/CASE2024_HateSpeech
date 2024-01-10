#!/bin/sh

# TF-IDF - lemma, stop
#python3 020_tfidf.py --train data/preprocessed/A-train.pre --test data/preprocessed/A-eval.pre --out A-eval --stop --lemma --pred
#python3 make_submission.py --pred data/pred_tfidf/A-eval.pred --base data/preprocessed/A-eval.pre --out A-tfidf.json

# BERT
mkdir -p data/pred_bert-large
CUDA_VISIBLE_DEVICES="" python3 lightning-text-classification/predict.py \
    --input data/preprocessed/A-eval.pre \
    --experiment data/bert-large-uncased-rte-1e-05-5e-05/A-5 \
    --output data/pred_bert-large/A-eval.pred
    #--experiment data/bert-large/A-5 \

python3 make_submission.py --pred data/pred_bert-large/A-eval.pred --base data/preprocessed/A-eval.pre --out A-bert.json

# DT
python3 080_prepare_data.py --base data/preprocessed/A-eval.pre --pred1 data/pred_tfidf/A-eval.pred --pred2 data/pred_bert-large/A-eval.pred --out data/folds/A-eval.combined
python3 090_decision_tree.py --train data/folds/A-5-test.combined --test data/folds/A-eval.combined --out A-eval --pred
python3 make_submission.py --pred data/pred_dt/A-eval.pred --base data/preprocessed/A-eval.pre --out A-dt.json
