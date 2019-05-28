# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:41:50 2018

@author: soren
"""

### vector file to z-score ###

# The Clinical terms, aging keywords, and the 994 words matrices were combined into the Aging_term_and_synonyms_and_word_list_binary.csv

#packages

import os
import pandas as pd
from scipy.stats import zscore

# Dictionaries #

Sub_in = "Word embeddings matrix"

Vector_file = "Clinical_term_and_Aging_keywords_and_word_list_binary.csv"

Zscore_file = "Zscore_matrix.csv"

### Calculate zscore and apply to data´

#Load data

Categorical_values = pd.read_csv(os.path.join(Sub_in,Vector_file),sep=";",encoding = 'cp1252')
print("data loaded.")

Zscore_values = Categorical_values.apply(zscore)
print("zscore calculated and applied.")

#save to file

Zscore_values.to_csv(os.path.join(Sub_in,Zscore_file), sep=';', encoding='utf-8',index=False)
print("data saved to zscore csv file.")
