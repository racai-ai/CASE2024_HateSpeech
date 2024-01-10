import numpy as np 
import pandas as pd
from sklearn import metrics, tree
import nltk
import re
import string
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
import argparse
import os 
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--base", help = "Base CSV", required=True)
parser.add_argument("--pred1", help = "Pred1 CSV", required=True)
parser.add_argument("--pred2", help = "Pred2 CSV", required=True)
parser.add_argument("--out", help = "Output", required=True)
args = parser.parse_args()

dataBase=pd.read_csv(args.base, sep='\t', header=0, keep_default_na=False, na_values=['_____________'])
dataBase=dataBase.drop(columns=["text"])
dataPred1=pd.read_csv(args.pred1, sep='\t', header=0, keep_default_na=False, na_values=['______________'])
dataPred2=pd.read_csv(args.pred2, sep='\t', header=0, keep_default_na=False, na_values=['________________'])

dataBase["tfidf"]=dataPred1.loc[:,["pred"]]
dataBase["bert"]=dataPred2.loc[:,["pred"]]

dataBase.to_csv(args.out,sep='\t', index=False)
