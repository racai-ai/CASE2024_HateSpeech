import numpy as np
import argparse
import os 
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--out", help = "Output base name for JSON", required=True)
parser.add_argument("files", help = "JSON files", nargs="+")
args = parser.parse_args()

if not os.path.exists("data/average"):
    os.makedirs("data/average") 

all_acc=[]
all_macro_f1=[]
all_weighted_f1=[]
for f in args.files:
    with open(f, 'r') as openfile:
        data = json.load(openfile)
        all_acc.append(data['accuracy'])
        all_macro_f1.append(data['macro avg']['f1-score'])
        all_weighted_f1.append(data['weighted avg']['f1-score'])

acc=np.average(all_acc)
macrof1=np.average(all_macro_f1)
weightf1=np.average(all_weighted_f1)

print("Average Accuracy: {acc:.2f}\nAverage Macro F1: {macro:.2f}\nAverage Weighted F1: {weight:.2f}".format(
    acc=acc, macro=macrof1, weight=weightf1))

with open("data/average/{out}.json".format(out=args.out),"w") as f:
    json.dump({
        "accuracy":{
            "average":acc,
            "min":np.min(all_acc),
            "max":np.max(all_acc),
            "std":np.std(all_acc),
        },
        "macro-f1":{
            "average":macrof1,
            "min":np.min(all_macro_f1),
            "max":np.max(all_macro_f1),
            "std":np.std(all_macro_f1),
        },
        "weighted-f1":{
            "average":weightf1,
            "min":np.min(all_weighted_f1),
            "max":np.max(all_weighted_f1),
            "std":np.std(all_weighted_f1),
        }

    },f,indent=4)
