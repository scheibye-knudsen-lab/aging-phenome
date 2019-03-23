# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:10:43 2019

@author: soren
"""

### Tf-idf normalization ###

#import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import os

# Dictionaries #

Sub_in = "Word embeddings matrix"

# files #
Vector_file = "Aging_term_and_synonyms_and_word_list_binary.csv"
TF_IDF_file = "TF_IDF_Matrix.csv"

# Variables #
Header_flag = 1
Count_Matrix = []

# load data #
with open(os.path.join(Sub_in,Vector_file),encoding = 'cp1252') as read:
    for line in read:
        line = line.strip().split(';')
        if Header_flag == 1:
            Header = line
            Header_flag = 0
        else:
            Count_Matrix.append(list(map(int,line)))
print("data loaded")

#initialize transformer
transformer = TfidfTransformer(smooth_idf=False)

#Transform count matrix to tfidf weighting
tfidf = transformer.fit_transform(Count_Matrix)
Weighted_Matrix = tfidf.toarray()

#Summerize weighted based on sum and mean
summarizer_default = lambda x: np.sum(x, axis=0)
summarizer_mean = lambda x: np.mean(x, axis=0)

Relevance_mean_score = summarizer_mean(Weighted_Matrix)
Relevance_default_score = summarizer_default(Weighted_Matrix)

#Save Weighted TF-IDF matrix to file
with open(os.path.join(Sub_in,TF_IDF_file),'w+',encoding = 'cp1252') as outfile:
    outfile.write("{}\n".format(";".join(Header)))
    for key in Weighted_Matrix:
        outfile.write("{}\n".format(";".join(map(str,key))))
outfile.close
print("TF_IDF_Matrix saved.")
