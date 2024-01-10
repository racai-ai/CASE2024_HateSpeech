import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
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
parser.add_argument("--pred", help = "Input CSV (must contain the column pred)", required=True)
parser.add_argument("--out", help = "Submission JSON", required=True)
parser.add_argument("--base", help = "Base CSV (must contain the column id)", required=True)
args = parser.parse_args()

if not os.path.exists("data/evaluation"): 
    os.makedirs("data/evaluation") 


dataIn = pd.read_csv(args.pred, sep='\t', header=0)
dataBase = pd.read_csv(args.base, sep='\t', header=0)

#dataIn=dataIn.loc[:,['pred']]
dataBase=dataBase.loc[:,['id']]

dataBase=dataBase.join(dataIn["pred"])
#dataBase.sort_values(by=['id'], inplace=True)

with open(os.path.join("data","evaluation",args.out),"w") as f:
    #f.write("[\n")
    for i,row in dataBase.iterrows():
        #if i>0: f.write(",\n")
        #f.write('    {{"index":{id}, "prediction":{pred}}}'.format(id=row["id"], pred=row["pred"]))
        f.write('{{"index":{id}, "prediction":{pred}}}\n'.format(id=row["id"], pred=row["pred"]))
    #f.write("\n]\n")

