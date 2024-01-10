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
parser.add_argument("--train", help = "Train CSV", required=True)
parser.add_argument("--test", help = "Test CSV", required=True)
parser.add_argument("--out", help = "Output base name for JSON and CSV (if pred)", required=True)
parser.add_argument("--pred", help = "Perform prediction", action='store_true')
args = parser.parse_args()

if not os.path.exists("data/pred_dt"): 
    os.makedirs("data/pred_dt") 

dataTrainRaw = pd.read_csv(args.train, sep='\t', header=0, keep_default_na=False, na_values=['________'])
dataTrainY = dataTrainRaw.loc[:,["label"]]
labels=[str(l) for l in dataTrainRaw.label.unique()]
columnsDrop=["id","label","RawSz","PreSz","DiffSz","Hashtags"]
dataTrain = dataTrainRaw.drop(columns=columnsDrop)

dataTestRaw = pd.read_csv(args.test, sep='\t', header=0, keep_default_na=False, na_values=['_____________'])
dataTest = dataTestRaw.drop(columns=columnsDrop)
#dataTest = dataTest.loc[:,['text','label']]

clf=tree.DecisionTreeClassifier()
clf.fit(dataTrain, dataTrainY)

y_pred = clf.predict(dataTest)

text_representation = tree.export_text(clf, feature_names=dataTest.columns)
print(text_representation)

from sklearn.tree import export_graphviz
# Export as dot file
export_graphviz(clf, out_file='tree.dot', 
                feature_names = dataTest.columns,
                #class_names = iris.target_names,
                rounded = True, proportion = False, 
                precision = 2, filled = True)

with open("data/pred_dt/{out}.params.json".format(out=args.out),"w") as f:
    json.dump(vars(args),f,indent=4)

if not args.pred:
    test_y=dataTestRaw.loc[:,["label"]]
    print(metrics.classification_report(test_y, y_pred, target_names=labels))

    print("Confusion matrix:")
    print(metrics.confusion_matrix(test_y, y_pred))

    res=metrics.classification_report(test_y, y_pred, target_names=labels, output_dict=True)
    with open("data/pred_dt/{out}.json".format(out=args.out),"w") as f:
        json.dump(res,f,indent=4)

else:
    dataTest['pred']=y_pred
    dataTest.to_csv('data/pred_dt/{out}.pred'.format(out=args.out),sep='\t', index=False)
