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

if not os.path.exists("data/pred_tfidf"): 
    os.makedirs("data/pred_tfidf") 

 
parser = argparse.ArgumentParser()
parser.add_argument("--lemma", help = "Lemmatization")
parser.add_argument("--stop", help = "Remove stop words")
args = parser.parse_args()

data = pd.read_csv('data/preprocessed/A-train.pre', sep='\t', header=0)
data = data.loc[:,['text','label']]
#print(data)


if args.stop:
    stopwords = nltk.corpus.stopwords.words('english')
    nltk.download('stopwords')

if args.lemma:
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()


def make_X_y(train):
    train_X_text = train['text'].to_numpy()
    train_y = train['label'].to_numpy()
    train_X = []

    for i in range(0,len(train_X_text)):
        text=train_X_text[i]
        if args.stop or args.lemma:
            text=text.split()
            if args.stop:
                text=[word for word in text if not word in set(stopwords)]
            if args.lemma:
                text=[lemmatizer.lemmatize(word) for word in text]
            text=' '.join(text)
        train_X.append(text)

    return (train_X, train_y)

all_acc=[]
all_macro=[]
all_weighted=[]
for i in range(1,10):
    print("Fold ",i)

    train, test = train_test_split(data, test_size=0.2)

    (train_X, train_y)=make_X_y(train)
    (test_X, test_y)=make_X_y(test)

    tf_idf = TfidfVectorizer()
    X_train_tf = tf_idf.fit_transform(train_X)
    X_train_tf = tf_idf.transform(train_X)

    X_test_tf = tf_idf.transform(test_X)

    X_test_tf = tf_idf.transform(test_X)

    print("TRAIN: n_samples: %d, n_features: %d" % X_train_tf.shape)
    print("TEST: n_samples: %d, n_features: %d" % X_test_tf.shape)

    naive_bayes_classifier = MultinomialNB()
    naive_bayes_classifier.fit(X_train_tf, train_y)
    y_pred = naive_bayes_classifier.predict(X_test_tf)

    print(metrics.classification_report(test_y, y_pred, target_names=['Positive', 'Negative']))

    print("Confusion matrix:")
    print(metrics.confusion_matrix(test_y, y_pred))

    res=metrics.classification_report(test_y, y_pred, target_names=['Positive', 'Negative'], output_dict=True)

    all_acc.append(res['accuracy'])
    all_macro.append(res['macro avg']['f1-score'])
    all_weighted.append(res['weighted avg']['f1-score'])


print("Average Accuracy: {acc:.2f}\nAverage Macro F1: {macro:.2f}\nAverage Weighted F1: {weight:.2f}".format(
    acc=np.average(all_acc), 
    macro=np.average(all_macro), 
    weight=np.average(all_weighted)))

print("Re-train on all data")
dataEvalOrig = pd.read_csv('data/preprocessed/A-eval.pre', sep='\t', header=0)
dataEval = dataEvalOrig.loc[:,['text','label']]
(train_X, train_y)=make_X_y(data)
(eval_X, eval_y)=make_X_y(dataEval)

tf_idf = TfidfVectorizer()
X_train_tf = tf_idf.fit_transform(train_X)
X_train_tf = tf_idf.transform(train_X)


X_eval_tf = tf_idf.transform(eval_X)

print("TRAIN: n_samples: %d, n_features: %d" % X_train_tf.shape)
print("EVAL: n_samples: %d, n_features: %d" % X_eval_tf.shape)

naive_bayes_classifier = MultinomialNB()
naive_bayes_classifier.fit(X_train_tf, train_y)
y_pred = naive_bayes_classifier.predict(X_eval_tf)

dataEval['pred']=y_pred
#dataEval.assign(pred=lambda x: y_pred[x.index])
dataEval.to_csv('data/pred_tfidf/A-eval-{stop}-{lemma}.pred'.format(stop=args.stop,lemma=args.lemma),sep='\t', index=False)
