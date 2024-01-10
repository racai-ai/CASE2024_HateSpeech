#!/bin/sh

export CUDA_VISIBLE_DEVICES="1"

PREPROCESS=false
FOLDS=false
TFIDF=false
BERT=true
DT=false

if [ "$PREPROCESS" = true ] ; then
    echo "Preprocessing"
    php 010_preprocess.php
fi

if [ "$FOLDS" = true ] ; then
    echo "Creating folds"
    python3 011_make_folds.py -f 10 -d data/preprocessed/A-train.pre -n A
fi

if [ "$TFIDF" = true ] ; then
    echo "Running TFIDF"

    # TF-IDF - no lemma, no stop
    files=""
    for i in {1..10}; do
        python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-test.csv --out A-$i
        files="$files data/pred_tfidf/A-$i.json"
    done
    python3 compute_average.py --out A-tfidf-average $files

    # TF-IDF - lemma, no stop
    files=""
    for i in {1..10}; do
        python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-test.csv --out A-lemma-$i --lemma
        files="$files data/pred_tfidf/A-lemma-$i.json"
    done
    python3 compute_average.py --out A-tfidf-lemma-average $files

    # TF-IDF - no lemma, stop
    files=""
    for i in {1..10}; do
        python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-test.csv --out A-stop-$i --stop
        files="$files data/pred_tfidf/A-stop-$i.json"
    done
    python3 compute_average.py --out A-tfidf-stop-average $files

    # TF-IDF - lemma, stop
    files=""
    for i in {1..10}; do
        python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-test.csv --out A-lemma-stop-$i --stop --lemma
        files="$files data/pred_tfidf/A-lemma-stop-$i.json"
    done
    python3 compute_average.py --out A-tfidf-lemma-stop-average $files
fi

if [ "$BERT" = true ] ; then
    echo "Training BERT"
    # BERT

    #for elr in "1e-05" "2e-05" "3e-05" "5e-05" "9e-06" ; do

    #for lr in "5e-05" "4e-05" "3e-05" "2e-05" "8e-05" ; do

    for elr in "3e-05" ; do

    for lr in "2e-05" ; do

    files=""

    modelbase="bert-large-uncased"
    model="$modelbase"

    #modelbase="bert-large-cased-finetuned-cola"
    #model="gchhablani/$modelbase"

    #modelbase="bert-large-uncased-rte" # GOOD
    #model="yoshitomo-matsubara/$modelbase"

    #modelbase="bert-large-uncased-stsb"
    #model="yoshitomo-matsubara/$modelbase"

    #modelbase="bert-large-uncased-Hate_Offensive_or_Normal_Speech" # bad
    #model="DunnBC22/$modelbase"

    for i in {1..10}; do
        echo "BERT A-$i ELR=$elr LR=$lr"
        #rm -fr data/bert-large/A-$i
        python3 lightning-text-classification/training.py \
            --gpus 1 \
            --train_csv data/folds/A-$i-train.csv \
            --test_csv data/folds/A-$i-test.csv \
            --dev_csv data/folds/A-$i-dev.csv \
            --min_epochs 5 \
            --nr_frozen_epochs 3 \
            --max_epochs 20 \
            --patience 3 \
            --encoder_learning_rate $elr \
            --learning_rate $lr \
            --encoder_model $model \
            --batch_size 64 \
            --accumulate_grad_batches 2 \
            --out "data/lstm2-$modelbase-$elr-$lr/A-$i" 
            #--monitor val_f1macro
#            --encoder_model bert-large-uncased \
#            --out data/bert-large/A-$i
#        files="$files data/bert-large/A-$i/test.json"
        files="$files data/lstm2-$modelbase-$elr-$lr/A-$i/test.json"
    done
#    python3 compute_average.py --out A-bert-large-average $files
    python3 compute_average.py --out A-lstm2-$modelbase-$elr-$lr-average $files

    done
    done

fi

if [ "$DT" = true ] ; then
    echo "Decision tree"
    files=""
    mkdir -p data/pred_bert-large
    mkdir -p data/pred_dt
    for i in {1..10}; do
        # PREDICT ON TRAIN

        #python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-train_all.csv --out A-$i-train_all.pred --stop --lemma --pred

        #CUDA_VISIBLE_DEVICES="" python3 lightning-text-classification/predict.py \
        #    --input data/folds/A-$i-train_all.csv \
        #    --experiment data/bert-large/A-5 \
        #    --output data/pred_bert-large/A-$i-train_all.pred

        #python3 080_prepare_data.py --base data/folds/A-$i-train_all.csv --pred1 data/pred_tfidf/A-$i-train_all.pred.pred --pred2 data/pred_bert-large/A-$i-train_all.pred --out data/folds/A-$i-train_all.combined

        # PREDICT ON TEST
        #python3 020_tfidf.py --train data/folds/A-$i-train_all.csv --test data/folds/A-$i-test.csv --out A-$i-test.pred --stop --lemma --pred

        #CUDA_VISIBLE_DEVICES="" python3 lightning-text-classification/predict.py \
        #    --input data/folds/A-$i-test.csv \
        #    --experiment data/bert-large/A-5 \
        #    --output data/pred_bert-large/A-$i-test.pred

        #python3 080_prepare_data.py --base data/folds/A-$i-test.csv --pred1 data/pred_tfidf/A-$i-test.pred.pred --pred2 data/pred_bert-large/A-$i-test.pred --out data/folds/A-$i-test.combined

        #python3 090_decision_tree.py --train data/folds/A-$i-train_all.combined --test data/folds/A-$i-test.combined --out A-$i-test
        python3 090_decision_tree.py --train data/folds/A-$i-test.combined --test data/folds/A-$i-test.combined --out A-$i-test-only
        files="$files data/pred_dt/A-$i-test-only.json"
    done
    python3 compute_average.py --out A-dt-test $files
fi
