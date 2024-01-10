import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folds", help = "Number of folds", default=10, type=int)
parser.add_argument("-d", "--data", help = "Data CSV", required=True)
parser.add_argument("-n", "--name", help = "Base name for output CSV", required=True)
args = parser.parse_args()

if not os.path.exists("data/folds"):
    os.makedirs("data/folds")

data = pd.read_csv(args.data, sep='\t', header=0)
#data = data.loc[:,['text','label']]

kf=KFold(n_splits=args.folds, shuffle=True)
fold=0
for train_index, test_index in kf.split(data):
    fold+=1
    X_train, X_test = data.iloc[train_index], data.iloc[test_index]
    X_train1, X_dev = train_test_split(X_train, test_size=0.2)
    X_train.to_csv('data/folds/{name}-{fold}-train_all.csv'.format(name=args.name,fold=fold),sep='\t', index=False)
    X_test.to_csv('data/folds/{name}-{fold}-test.csv'.format(name=args.name,fold=fold),sep='\t', index=False)
    X_train1.to_csv('data/folds/{name}-{fold}-train.csv'.format(name=args.name,fold=fold),sep='\t', index=False)
    X_dev.to_csv('data/folds/{name}-{fold}-dev.csv'.format(name=args.name,fold=fold),sep='\t', index=False)
